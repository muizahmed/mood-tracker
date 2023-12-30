## Script for Dummy Data

from cs50 import SQL
import random
from datetime import datetime, timedelta

user_id = 14
dummy_text = "dummy text"

start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 31)


db = SQL("sqlite:///EmoTracker.db")

for id in range(300, 320):
    # Generate random dates
    random_number_of_days = random.randint(0, (end_date - start_date).days)
    random_date = (start_date + timedelta(days=random_number_of_days)).date()

    date_set = set()
    while random_date in date_set:
        random_number_of_days = random.randint(0, (end_date - start_date).days)
        random_date = (start_date + timedelta(days=random_number_of_days)).date()
    date_set.add(random_date)

    db.execute("INSERT INTO Entry VALUES (?, ?, ?)", id, user_id, random_date)

    max = 100
    for mood_id in range(1, 8):
        percentage = random.randint(1, 20)
        db.execute("INSERT INTO User_Mood VALUES(?, ?, ?, ?)", id, mood_id, percentage, dummy_text)

