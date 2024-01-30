# EmoTracker

### Overview
EmoTracker is a Mood Tracker web application designed to help you monitor and understand your emotions over time. It provides a simple and intuitive interface for logging your daily moods, along with reasons for each emotion. With insightful features and a user-friendly design, EmoTracker aims to enhance your self-awareness and emotional well-being.

### Demo
Check out our [Video Demo](https://youtu.be/ZMu5udibQhc) to see EmoTracker in action.

### Live Deployment
Explore EmoTracker live on [Heroku](https://emo-tracker-de9598ceb310.herokuapp.com).

## Features
- **Mood Tracking:** Log your daily emotions with a range slider for each mood.
- **Reason Logging:** Provide reasons for each emotion to better understand your feelings.
- **Historical Insights:** View your mood logs for the past 31 days and consecutive days streak.
- **Monthly Overview:** Get an overview of your emotional trends for the past month.
- **Date-specific View:** Navigate to a specific day to review your mood entries.

## Usage

1. **Registration:** Create a user account using the Register link in the top-right corner. Provide your name, a unique username, and set a preferred app address.

2. **Login:** After registration, log in using your newly created account.

3. **Mood Logging:** Slide the range slider to set values for each emotion. Enter a reason for emotions with values greater than 0. The sum of all emotions should not exceed 100.

4. **Date Picker:** Access the `date-view` page to pick a specific date and view mood logs for that day.

5. **Insights:** Gain insights on the homepage, including top 3 moods, happiest day, saddest day, and angriest day for the past month.

## Implementation

EmoTracker is a single-page web app developed using Python, SQL, Flask, and Jinja for functionality. The front-end utilizes HTML, CSS, and JS.

### Database Structure
- **Users Table:** Tracks user information, including name, password hash, and current streak.
- **Entry Table:** Records entry details such as `entry_id` and entry date.
- **Moods Table:** Contains default moods with unique IDs and an uncategorized mood for incomplete emotional sums.
- **User_Mood Table:** Manages user mood entries, storing mood percentages and reasons.

### Technologies Used
- **Backend:** Python, SQL, Flask, Jinja
- **Frontend:** HTML, CSS, JS

Feel free to explore and use EmoTracker to gain insights into your emotional well-being. If you encounter any issues or have suggestions, don't hesitate to reach out. Happy mood tracking!
