import sqlite3
from datetime import datetime, timedelta

class Habit:
    """
    Represents a habit with a task specification, periodicity, habit period, and completion history.

    Attributes:
    - name (str): The name of the habit.
    - task (str): The task associated with the habit.
    - periodicity (int): The frequency at which the habit should be completed (in days).
    - habit_period (str): The habit period ('daily' or 'weekly').
    - completed_dates (list of datetime): Dates on which the habit was completed.
    """

    def __init__(self, name, task, periodicity, habit_period):
        """
        Initialize a new Habit.

        Parameters:
        - name (str): The name of the habit.
        - task (str): The task associated with the habit.
        - periodicity (int): The frequency at which the habit should be completed (in days).
        - habit_period (str): The habit period ('daily' or 'weekly').
        """
        self.name = name
        self.task = task
        self.periodicity = periodicity
        self.habit_period = habit_period
        self.completed_dates = []

    def complete_task(self):
        """
        Mark the habit as completed on the current date and time.
        """
        self.completed_dates.append(datetime.now())

    def is_habit_broken(self, current_date):
        """
        Check if the habit is broken based on the last completed date.

        Parameters:
        - current_date (datetime): The current date.

        Returns:
        - bool: True if the habit is broken, False otherwise.
        """
        return current_date - self.completed_dates[-1] > timedelta(days=self.periodicity)

    def get_current_streak(self, current_date):
        """
        Get the current streak of completing the habit.

        Parameters:
        - current_date (datetime): The current date.

        Returns:
        - int: The current streak of completing the habit.
        """
        streak = 0
        while self.is_habit_broken(current_date - timedelta(days=streak)):
            streak += 1
        return streak

class HabitTracker:
    """
    Manages a collection of habits and provides analysis methods.

    Attributes:
    - habits (list of Habit): List of habits tracked by the app.
    """

    def __init__(self):
        """Initialize a new HabitTracker with an empty list of habits."""
        self.habits = []
        self.db_connection = sqlite3.connect('habit_tracker.db')
        self.create_tables()

    def create_tables(self):
        """Create necessary tables in the SQLite database."""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                name TEXT,
                task TEXT,
                periodicity INTEGER,
                habit_period TEXT,
                completed_dates TEXT
            )
        ''')
        self.db_connection.commit()

    def save_habit_to_db(self, habit):
        """Save a habit to the SQLite database."""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO habits (name, task, periodicity, habit_period, completed_dates)
            VALUES (?, ?, ?, ?, ?)
        ''', (habit.name, habit.task, habit.periodicity, habit.habit_period, str(habit.completed_dates)))
        self.db_connection.commit()

    def load_habits_from_db(self):
        """Load habits from the SQLite database."""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM habits')
        rows = cursor.fetchall()
        for row in rows:
            habit = Habit(row[0], row[1], row[2], row[3])
            habit.completed_dates = eval(row[4])  # Convert string representation back to a list
            self.habits.append(habit)

    def add_habit(self, habit):
        """
        Add a habit to the tracker.

        Parameters:
        - habit (Habit): The habit to be added.
        """
        self.habits.append(habit)
        self.save_habit_to_db(habit)

    def get_current_daily_habits(self):
        """
        Get the list of daily habits that are currently being followed.

        Returns:
        - list of str: List of daily habit names currently being followed.
        """
        current_date = datetime.now()
        current_habits = [habit.name for habit in self.habits if habit.habit_period == 'daily' and not habit.is_habit_broken(current_date)]
        return current_habits

    def get_current_weekly_habits(self):
        """
        Get the list of weekly habits that are currently being followed.

        Returns:
        - list of str: List of weekly habit names currently being followed.
        """
        current_date = datetime.now()
        current_habits = [habit.name for habit in self.habits if habit.habit_period == 'weekly' and not habit.is_habit_broken(current_date)]
        return current_habits

    def get_all_habits_with_periodicity(self, habit_period):
        """
        Get the list of habits with the specified periodicity.

        Parameters:
        - habit_period (str): The habit period ('daily' or 'weekly').

        Returns:
        - list of str: List of habit names with the specified periodicity.
        """
        return [habit.name for habit in self.habits if habit.habit_period == habit_period]

    def get_longest_run_streak_of_all_habits(self):
        """
        Get the longest run streak among all defined habits.

        Returns:
        - int: The longest run streak among all defined habits.
        """
        longest_streak = 0
        for habit in self.habits:
            current_streak = habit.get_current_streak(datetime.now())
            if current_streak > longest_streak:
                longest_streak = current_streak
        return longest_streak

    def get_longest_run_streak_for_habit(self, habit_name):
        """
        Get the longest run streak for a given habit.

        Parameters:
        - habit_name (str): The name of the habit.

        Returns:
        - int: The longest run streak for the given habit.
        """
        habit = next((h for h in self.habits if h.name == habit_name), None)
        if habit:
            return habit.get_current_streak(datetime.now())
        else:
            return 0
        


    def add_habit_from_input(self):
        """Add a habit to the tracker based on user input."""
        name = input("Enter habit name: ")
        task = input("Enter associated task: ")
        periodicity = int(input("Enter frequency (in days): "))
        habit_period = input("Enter habit period ('daily' or 'weekly'): ")

        new_habit = Habit(name, task, periodicity, habit_period)
        self.add_habit(new_habit)
        print(f"Habit '{name}' added successfully.")

    def show_current_daily_habits(self):
        """Show the list of daily habits currently being followed."""
        print("Current daily habits:")
        print(self.get_current_daily_habits())

    def show_current_weekly_habits(self):
        """Show the list of weekly habits currently being followed."""
        print("Current weekly habits:")
        print(self.get_current_weekly_habits())

    def show_longest_run_streaks(self):
        """Show the longest run streaks for all habits."""
        print("Longest run streaks:")
        for habit in self.habits:
            print(f"{habit.name}: {self.get_longest_run_streak_for_habit(habit.name)} days")

# Example Usage
if __name__ == "__main__":
    tracker = HabitTracker()

    while True:
        print("\nOptions:")
        print("1. Add Habit")
        print("2. Show Current Daily Habits")
        print("3. Show Current Weekly Habits")
        print("4. Show Longest Run Streaks")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            tracker.add_habit_from_input()
        elif choice == "2":
            tracker.show_current_daily_habits()
        elif choice == "3":
            tracker.show_current_weekly_habits()
        elif choice == "4":
            tracker.show_longest_run_streaks()
        elif choice == "5":
            tracker.close_db_connection()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


    def close_db_connection(self):
        """Close the SQLite database connection."""
        self.db_connection.close()

# Example Usage
daily_habit = Habit("Exercise", "Go for a run", 1, "daily")
weekly_habit = Habit("Read", "Read a chapter", 7, "weekly")

tracker = HabitTracker()
tracker.add_habit(daily_habit)
tracker.add_habit(weekly_habit)

# Simulate tracking data for a period of 4 weeks
for _ in range(4 * 7):
    daily_habit.complete_task()
    weekly_habit.complete_task()

tracker.save_habit_to_db(daily_habit)
tracker.save_habit_to_db(weekly_habit)
tracker.close_db_connection()

print(tracker.get_all_habits_with_periodicity("daily"))
print(tracker.get_current_daily_habits())
print(tracker.get_current_weekly_habits())
print(tracker.get_longest_run_streak_for_habit("Documentary"))
print(tracker.get_longest_run_streak_of_all_habits())



