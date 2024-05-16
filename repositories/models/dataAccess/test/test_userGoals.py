import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from psycopg2.extras import Json
import userGoals

class TestUserGoalsDB(unittest.TestCase):
    def setUp(self):
        self.valid_user_id = 1
        self.valid_goal_data = {
            "goalDetails": {
                "title": "Learn Python",
                "description": "Complete Python course",
                "status": "In Progress",
                "motivationLevel": 5,
                "importance": "High",
                "dueDate": "2023-12-31",
                "overviewStatement": "Complete all modules"
            }
        }

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_create_goal_successful(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]  # Mocking goal_id returned by DB

        goal_id = user_goals.UserGoalsDB.create_goal(self.valid_user_id, self.valid_goal_data)
        self.assertEqual(goal_id, 1)

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    @patch('user_goals.UserGoalsValidator.validate_goal_data')
    def test_create_goal_validation_error(self, mock_validate, mock_cursor):
        # Configure the mock to raise a ValueError for invalid motivation level
        invalid_goal_data = {**self.valid_goal_data, "goalDetails": {**self.valid_goal_data["goalDetails"], "motivationLevel": 11}}
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]  # Mock a valid goal_id return
        mock_validate.side_effect = ValueError("Invalid motivation level")  # Raise ValueError

        with self.assertRaises(Exception) as context:
            user_goals.UserGoalsDB.create_goal(self.valid_user_id, invalid_goal_data)

        self.assertTrue("Invalid motivation level" in str(context.exception))
        mock_validate.assert_called_once()

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_update_goal_detail_successful(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        user_goals.UserGoalsDB.update_goal_detail(1, 'motivationLevel', 9)  # Valid update

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_update_goal_detail_validation_error(self, mock_cursor):
        with self.assertRaises(Exception):
            user_goals.UserGoalsDB.update_goal_detail(1, 'motivationLevel', 15)  # Invalid motivation level

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_get_goal_detail_successful(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ['Completed']  # Mocking fetched goal detail
        result = user_goals.UserGoalsDB.get_goal_detail(1, 'status')
        self.assertEqual(result, 'Completed')

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_get_goal_detail_nonexistent(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # No data found
        result = user_goals.UserGoalsDB.get_goal_detail(1, 'nonexistent_key')
        self.assertIsNone(result)

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_delete_goal_detail_successful(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        # No exception is expected to be raised
        try:
            user_goals.UserGoalsDB.delete_goal_detail(1, 'status')
        except Exception as e:
            self.fail(f"Delete goal detail raised an exception: {e}")

    @patch('user_goals.UserGoalsDB.get_db_cursor')
    def test_database_error_handling(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.side_effect = Exception("Database Error")  # Simulating database error
        with self.assertRaises(Exception) as context:
            user_goals.UserGoalsDB.create_goal(self.valid_user_id, {"goalDetails": {"title": "Learn Python"}})
        self.assertTrue('Failed to create goal' in str(context.exception))

class TestUserGoalsValidator(unittest.TestCase):
    def test_validate_goal_data_successful(self):
        valid_goal_data = {
            "goalDetails": {
                "title": "Learn Python",
                "description": "Complete Python course",
                "status": "In Progress",
                "motivationLevel": 5,
                "importance": "High",
                "dueDate": "2023-12-31",
                "overviewStatement": "Complete all modules"
            },
            "progressTracking": {
                "totalSteps": 10,
                "completedSteps": 5,
                "skippedSteps": 0
            }
        }
        try:
            user_goals.UserGoalsValidator.validate_goal_data(1, valid_goal_data)  # Should not raise an exception
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_validate_goal_data_invalid_user_id(self):
        with self.assertRaises(ValueError):
            user_goals.UserGoalsValidator.validate_goal_data('one', {})  # User ID must be an integer

if __name__ == '__main__':
    unittest.main()
