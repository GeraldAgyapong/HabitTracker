import unittest
from habit_tracker import Habit, HabitTracker

class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        # Initialize a test HabitTracker instance
        self.tracker = HabitTracker()

    def tearDown(self):
        # Close the database connection after each test
        self.tracker.close_db_connection()

    def test_habit_creation_and_completion(self):
        daily_habit = Habit("Exercise", "Go for a run", 1, "daily")
        weekly_habit = Habit("Read", "Read a chapter", 7, "weekly")

        self.tracker.add_habit(daily_habit)
        self.tracker.add_habit(weekly_habit)

        # Simulate completing tasks for a period
        for _ in range(7):
            daily_habit.complete_task()
            weekly_habit.complete_task()

        self.assertEqual(len(daily_habit.completed_dates), 7)
        self.assertEqual(len(weekly_habit.completed_dates), 7)

    def test_habit_tracking_analysis(self):
        daily_habit = Habit("Exercise", "Go for a run", 1, "daily")
        weekly_habit = Habit("Read", "Read a chapter", 7, "weekly")

        self.tracker.add_habit(daily_habit)
        self.tracker.add_habit(weekly_habit)

        # Simulate completing tasks for a period
        for _ in range(14):
            daily_habit.complete_task()

        for _ in range(35):
            weekly_habit.complete_task()

        # Save habits to the database
        self.tracker.save_habit_to_db(daily_habit)
        self.tracker.save_habit_to_db(weekly_habit)

        # Load habits from the database
        self.tracker.load_habits_from_db()

        # Test analytics functions
        self.assertEqual(self.tracker.get_longest_run_streak_of_all_habits(), 14)
        self.assertEqual(self.tracker.get_longest_run_streak_for_habit("Exercise"), 14)
        self.assertEqual(self.tracker.get_longest_run_streak_for_habit("Read"), 35)
        self.assertEqual(self.tracker.get_current_daily_habits(), ["Exercise"])
        self.assertEqual(self.tracker.get_current_weekly_habits(), ["Read"])

    def test_habit_periodicity_filter(self):
        daily_habit = Habit("Exercise", "Go for a run", 1, "daily")
        weekly_habit = Habit("Read", "Read a chapter", 7, "weekly")

        self.tracker.add_habit(daily_habit)
        self.tracker.add_habit(weekly_habit)

        daily_habits = self.tracker.get_all_habits_with_periodicity("daily")
        weekly_habits = self.tracker.get_all_habits_with_periodicity("weekly")

        self.assertEqual(daily_habits, ["Exercise"])
        self.assertEqual(weekly_habits, ["Read"])

if __name__ == '__main__':
    unittest.main()
