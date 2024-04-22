import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import user_context

class TestUserContextDB(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.context_id = 123
        self.context = {
            "permanent": {"userBackstory": "An interesting tale", "lifestylePreferences": [], "motivationalTriggers": [], "preferredTone": "friendly"},
            "temporal": {"userMood": "Happy", "moodRelevance": True, "lastMessageDate": "2021-01-01", "lastMessageCount": 5, "lastMessageHistory": []}
        }
        self.key = "userMood"
        self.value = "Excited"

    @patch('user_context.UserContextValidator.validate_context')
    @patch('user_context.UserContextDB.get_db_cursor')
    def test_create_context(self, mock_cursor, mock_validate):
        mock_conn = mock_cursor.return_value.__enter__.return_value
        mock_conn.fetchone.return_value = [self.context_id]
        context_id = user_context.UserContextDB.create_context(self.user_id, self.context)
        mock_validate.assert_called_once_with(self.context)
        mock_conn.execute.assert_called_once()
        self.assertEqual(context_id, self.context_id)

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_update_context_detail(self, mock_cursor):
        mock_conn = mock_cursor.return_value.__enter__.return_value
        user_context.UserContextDB.update_context_detail(self.context_id, self.key, self.value)
        mock_conn.execute.assert_called_once()

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_get_context_detail(self, mock_cursor):
        expected_value = "Excited"
        mock_conn = mock_cursor.return_value.__enter__.return_value
        mock_conn.fetchone.return_value = [expected_value]
        result = user_context.UserContextDB.get_context_detail(self.context_id, self.key)
        mock_conn.execute.assert_called_once()
        self.assertEqual(result, expected_value)

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_delete_context_detail(self, mock_cursor):
        mock_conn = mock_cursor.return_value.__enter__.return_value
        user_context.UserContextDB.delete_context_detail(self.context_id, self.key)
        mock_conn.execute.assert_called_once()

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_get_context(self, mock_cursor):
        expected_context = {"userMood": "Happy"}
        mock_conn = mock_cursor.return_value.__enter__.return_value
        mock_conn.fetchone.return_value = [expected_context]
        result = user_context.UserContextDB.get_context(self.context_id)
        mock_conn.execute.assert_called_once()
        self.assertEqual(result, expected_context)

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_delete_context(self, mock_cursor):
        mock_conn = mock_cursor.return_value.__enter__.return_value
        user_context.UserContextDB.delete_context(self.context_id)
        mock_conn.execute.assert_called_once()

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_create_context_exception_handling(self, mock_cursor):
        mock_cursor.return_value.__enter__.side_effect = Exception("Database error")
        with self.assertRaises(Exception) as context:
            user_context.UserContextDB.create_context(self.user_id, self.context)
        self.assertTrue('Database error' in str(context.exception))

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_update_context_detail_exception_handling(self, mock_cursor):
        mock_cursor.return_value.__enter__.side_effect = Exception("Update error")
        with self.assertRaises(Exception) as context:
            user_context.UserContextDB.update_context_detail(self.context_id, self.key, self.value)
        self.assertTrue('Update error' in str(context.exception))

    @patch('user_context.UserContextDB.get_db_cursor')
    def test_delete_context_exception_handling(self, mock_cursor):
        mock_cursor.return_value.__enter__.side_effect = Exception("Delete error")
        with self.assertRaises(Exception) as context:
            user_context.UserContextDB.delete_context(self.context_id)
        self.assertTrue('Delete error' in str(context.exception))

class TestUserContextValidator(unittest.TestCase):

    def test_validate_context(self):
        context = {
            "permanent": {"userBackstory": "Story", "lifestylePreferences": [], "motivationalTriggers": [], "preferredTone": "casual"},
            "temporal": {"userMood": "happy", "moodRelevance": True, "lastMessageDate": "2022-01-01", "lastMessageCount": 1, "lastMessageHistory": []}
        }
        try:
            user_context.UserContextValidator.validate_context(context)
        except ValueError as e:
            self.fail(f"validate_context raised ValueError unexpectedly: {e}")

    def test_invalid_permanent_section(self):
        context = {
            "permanent": {"userBackstory": 123, "lifestylePreferences": "not a list", "motivationalTriggers": "not a list", "preferredTone": 456},
            "temporal": {"userMood": "happy", "moodRelevance": True, "lastMessageDate": "2022-01-01", "lastMessageCount": 1, "lastMessageHistory": []}
        }
        with self.assertRaises(ValueError):
            user_context.UserContextValidator.validate_context(context)

    def test_invalid_temporal_section(self):
        context = {
            "permanent": {"userBackstory": "Story", "lifestylePreferences": [], "motivationalTriggers": [], "preferredTone": "casual"},
            "temporal": {"userMood": 789, "moodRelevance": "not bool", "lastMessageDate": 123, "lastMessageCount": "not int", "lastMessageHistory": "not list"}
        }
        with self.assertRaises(ValueError):
            user_context.UserContextValidator.validate_context(context)

    def test_missing_fields_in_permanent_section(self):
        context = {
            "permanent": {},
            "temporal": {"userMood": "happy", "moodRelevance": True, "lastMessageDate": "2022-01-01", "lastMessageCount": 1, "lastMessageHistory": []}
        }
        user_context.UserContextValidator.validate_context(context)
        self.assertEqual(context['permanent']['userBackstory'], "")

    def test_missing_fields_in_temporal_section(self):
        context = {
            "permanent": {"userBackstory": "Story", "lifestylePreferences": [], "motivationalTriggers": [], "preferredTone": "casual"},
            "temporal": {}
        }
        user_context.UserContextValidator.validate_context(context)
        self.assertFalse(context['temporal']['moodRelevance'])


if __name__ == '__main__':
    unittest.main()
