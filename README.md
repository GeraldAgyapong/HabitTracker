Habit Tracker ReadMe
Habit Tracker App

The Habit Tracker App is a Python-based application designed to help users track their daily and weekly habits, analyze their habits' streaks, and store habit data in an SQLite database.

Features

Habit Creation: Users can define multiple habits, specifying the task and periodicity (daily or weekly).
Task Completion: Users can mark tasks as completed, checking off habits at any time.
Habit Analysis: Provides insights such as the longest streak, current daily habits, and habits with the most struggle in the last month.
SQLite Database: Stores and retrieves habit data between sessions.
Command Line Interface (CLI): Offers a user-friendly command line interface for easy interaction.

Installation

1. Clone the Repository:
   git clone https://github.com/GeraldAgyapong/HabitTracker
   cd habit_tracker
   

2. Install Dependencies
   pip install -r requirements.txt

Usage

1.Run the Application:
   python habit_tracker.py

2. Command Line Interface (CLI) Commands:
   print(“get_current_daily_habits”): Lists current daily habits.
print(“get_current_weekly_habits”): Lists current weekly habits.
   print(get_longest_run_streak_for_all_habits): Shows the longest run streak among all defined habits.
   print (get_longest_run_streak_for_habit(habit name)): Shows the longest run streak for a specific habit.

## Example

bash
python habit_tracker.py get_current_daily_habits()

Output:
Current Daily Habits:
1. Exercise - Go for a run
2. Meditate - 10 minutes mindfulness


If you don't have the repository URL, you can obtain it from the GitHub page of the Habit Tracker app. Look for the "Code" button on the GitHub page, and copy the repository URL. Use this URL in the git clone command as mentioned in step 1.
