from cs50 import SQL
from flask import Flask, redirect, render_template, request, url_for, abort, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import itertools
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///EmoTracker.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


date_format = "%Y-%m-%d"

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Query database for username
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        # Get data from login form
        username = request.form.get("username").lower()
        password = request.form.get("password")

        rows = db.execute(
            "SELECT * FROM Users WHERE username = ?", username
        )

        # Check username and password
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            flash("Username or password incorrect!")
            return redirect(url_for("login"))

        # Save User ID
        session["user_id"] = rows[0]["id"]
        session["entry_exists"] = False
        return redirect("/")

    # If GET request, display login page
    else:
        register_user = request.args.get("new_user", default=False, type=bool)
        user_exists = request.args.get("user_exists", default=False, type=bool)
        if user_exists:
            register_user = True
        return render_template("login.html", register_user=register_user, user_exists=user_exists)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""

    if request.method == "POST":
        name = request.form.get("name").title()
        username = request.form.get("username").lower()
        ## Check if username already exists
        duplicate = db.execute("SELECT * FROM Users WHERE username = ?", username)
        if duplicate:
            return redirect(url_for("login", user_exists=True))

        password = request.form.get("password")

        db.execute(
            "INSERT INTO Users ('name', 'username', 'hash') VALUES (?, ?, ?)",
            name, username,
            generate_password_hash(password),
        )

        flash("Successfully registered! Please login now.", "info")
        return redirect(url_for("login"))

    # Alter the login page for registeration
    else:
        return redirect(url_for("login", new_user=True))


@app.route("/logout")
@login_required
def logout():
    """Log a user out"""

    session.clear()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Display the web app's Homepage/Dashboard"""

    global date_format

    user_id = session["user_id"]

    # Get relavant data from the database to display on homepage
    moods = db.execute("SELECT * FROM Moods")
    username = db.execute("SELECT name FROM Users WHERE id = ?", user_id)[0][
        "name"
    ]
    streak = db.execute("SELECT streak FROM Users WHERE id = ?", user_id)[0]["streak"]
    total_entries = db.execute(
        "SELECT COUNT(*) AS count FROM Entry \
                               WHERE Entry.date >= date('now', '-1 month') \
                                AND user_id = ?", user_id
    )[0]["count"]
    current_date = datetime.now().strftime("%B %d, %Y")

    moods_avg = {}
    moods_max = {}

    # Average percentage of top three moods
    if total_entries > 10:
        for mood_id in range(1, 8):
            current = db.execute(
                "SELECT ROUND(AVG(percentage)) AS avg, Moods.mood FROM User_Mood \
                    JOIN Moods ON User_Mood.mood_id = Moods.id \
                    JOIN Entry ON User_Mood.entry_id = Entry.id \
                        WHERE mood_id = ? AND user_id = ? \
                            AND Entry.date >= date('now', '-1 month')",
                mood_id,
                user_id,
            )[0]
            moods_avg[current["mood"]] = int(current["avg"])
        moods_avg = dict(
            sorted(moods_avg.items(), key=lambda item: item[1], reverse=True)
        )
        moods_avg = dict(itertools.islice(moods_avg.items(), 3))

        # Max values of happy, sad, and angry
        for mood_id in range(1, 4):
            current = db.execute(
                "SELECT MAX(percentage) AS max, Moods.mood, Entry.date FROM User_Mood \
                      JOIN Moods ON User_Mood.mood_id = Moods.id \
                      JOIN Entry ON User_Mood.entry_id = Entry.id \
                        WHERE mood_id = ? AND user_id = ? \
                            AND Entry.date >= date('now', '-1 month')",
                mood_id,
                user_id,
            )[0]
            moods_max[current["mood"]] = datetime.strptime(
                current["date"], date_format
            ).strftime("%A, %d %B")

    # Display the homepage if GET
    if request.method == "GET":
        return render_template(
            "index.html",
            total_entries=total_entries,
            date=current_date,
            moods=moods,
            avg=moods_avg,
            max=moods_max,
            streak=streak,
            username=username,
            entry_exists=session["entry_exists"],
        )

    # Process and insert the data if POST (form submitted)
    else:
        # Create an entry for current user on current date, and get the entry_id
        ## If entry already exists for today, throw an error
        if session["entry_exists"]:
            flash("You've already logged your mood for today!")
            return redirect(url_for("index"))

        ## Check user streak
        today = datetime.now().strftime(date_format)
        prev_date = db.execute(
            "SELECT date FROM Entry WHERE user_id = ? ORDER BY date DESC LIMIT 1",
            user_id,
        )
        if prev_date:
            prev_date = prev_date[0]["date"]
        else:  # If this is the first entry of the user
            prev_date = today

        substreak = (
            datetime.strptime(today, date_format)
            - datetime.strptime(prev_date, date_format)
        ).days
        if substreak == 1:
            db.execute("UPDATE Users SET streak = streak + 1 WHERE id = ?", user_id)
        elif substreak == 0:
            db.execute("UPDATE Users SET streak = 1 WHERE id = ?", user_id)
        else:
            db.execute("UPDATE Users SET streak = 0 WHERE id = ?", user_id)

        db.execute(
            "INSERT INTO Entry (user_id, date) VALUES (?, CURRENT_DATE)", user_id
        )

        entry_id = db.execute("SELECT id FROM Entry ORDER BY id DESC LIMIT 1")[0]["id"]

        total_value = 0

        # Loop through the moods list to insert data for each mood_id
        for mood in moods:
            mood_id = mood["id"]

            # If mood is anything apart from uncategorized, get the data from the form
            if mood["mood"] != "uncategorized":
                percentage = int(request.form.get(f"{mood['mood']}Percentage"))
                total_value += percentage

                # If the user changed the default value for a mood, get its associated reason from the form
                if percentage != 0:
                    reason = request.form.get(f"{mood['mood']}Reason")
                # Else enter NULL for reason
                else:
                    reason = None

            # If the total sum of user's mood percentages is less than 100, the remaining is uncategorized
            elif mood["mood"] == "uncategorized":
                percentage = 100 - total_value
                reason = None

            # Add data to the table
            db.execute(
                "INSERT INTO User_Mood VALUES (?, ?, ?, ?)",
                entry_id,
                mood_id,
                percentage,
                reason,
            )

        session["entry_exists"] = True
        return redirect("/")


@app.route("/date-view", methods=["GET", "POST"])
@login_required
def date_view():
    if request.method == "POST":
        date = request.form.get("date")
        return redirect(url_for("show_date_view", date=date))
    return render_template("date-view.html")


@app.route("/date-view/<date>", methods=["GET"])
@login_required
def show_date_view(date):
    user_id = session["user_id"]
    try:
        formatted_date = (datetime.strptime(date, date_format)).strftime(
            "%B %d, %Y"
        )  # Try to parse the date
    except ValueError:
        flash("Invalid date format. Please pick a date from below")
        return redirect(url_for("date_view"))

    data = db.execute(
        "SELECT Moods.mood, User_Mood.percentage, User_Mood.reason FROM User_Mood \
                        JOIN Moods ON User_Mood.mood_id = Moods.id \
                        JOIN Entry ON User_Mood.entry_id = Entry.id \
                        WHERE user_id = ? AND Entry.date = ? \
                        AND User_Mood.percentage > 0",
        user_id,
        date,
    )
    if not data:
        flash("Sorry, no data found! Pick another date")
        return redirect(url_for("date_view"))
    return render_template("show-date-view.html", date=formatted_date, data=data)


@app.template_filter("zip")
def zip_lists(a, b):
    return zip(a, b)

if __name__ == "__main__":
    app.run(debug=True)
