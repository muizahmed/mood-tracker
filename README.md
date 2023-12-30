# EmoTracker
#### Video Demo: https://youtu.be/ZMu5udibQhc
#### Description: A Mood Tracker that tracks percentages of emotions you felt today, along with reason for each of the emotion

## Features
- Tracks mood/emotion
- Tracks reason for each emotion
- Maintains track of how many days you logged your mood in the past 31 days
- Maintains track of how many consecuetive days you logged your mood
- Provides an overview of how you have felt over the past month
- Allows you to go to a specific day and see your mood tracking for that day


## Usage

First, you need to create a User using the Register link located in the top-right of the navigation bar, using which you can then login to your brand new account. Provide a name by which you'd prefer to be addressed by the app, as well as a unique username.

Once a User is created, you're now ready to log your mood and make the first entry.

You'll need to slide the range slider to your desired value for each emotion. The slider thumb will change to display the current value once it is interacted with. You must enter a reason for each emotion that has a value greater than 0. The sum of all emotions cannot exceed 100, and once it has, the sliders will freeze.

Once an entry has been made for today, you cannot make another entry, and if you try to, you'll be directed to the homepage and shown an error message.

You can also go the `date-view` page by clicking View Data in the navigation bar, which will take you to a Date Picker, where you can pick the date that you want to view the logs for. If no logs exist for that date, you'll be shown an error message and prompted to pick another date.
If logs do exist for that date, you'll be taken to a dynamic URL for that date, and shown the logs in a nicely formatted table.

Apart from logging mood, you can also see some insights on the homepage once you have made a couple of entries. You'll be shown your top 3 moods for the past month, as well as the days you felt the most happy, the most sad, and the most angry.

## Implementation

EmoTracker is a single-paged web app that uses Python, SQL, alongside Flask and Jinja for its functionality.

It uses plain HTML, CSS, and JS for the front-end.

The SQL Database EmoTracker.db has 5 tables: `Entry`, `Moods`, `User_Mood`, and `Users`.

The `Users` table keeps track of the user's name, their hash for password (not implemented yet), and their current ongoing streak (set to `0` by default).

The `Entry` table keeps track of `entry_id` for each entry made, as well as the date that the entry was made on.

The `Moods` table is a table that has 7 default moods, which get rendered on the homepage, and they each have their unique ID. It also has an uncatogerized mood, where if the sum of your emotions doesn't add up to 100, the rest is considered uncatogerized.

Lastly, the `User_Mood` table is where all the magic happens, and it keeps track of the mood and percentage of mood and reason for each user.
