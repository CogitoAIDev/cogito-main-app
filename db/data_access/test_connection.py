import os
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from connection import DatabaseConnectionPool

# Load environment variables
load_dotenv()

class TestDatabaseConnectionPool(unittest.TestCase):

    def setUp(self):
        self.mock_pool = MagicMock()
        with patch('connection.pool.SimpleConnectionPool', return_value=self.mock_pool):
            self.db_pool = DatabaseConnectionPool()
            DatabaseConnectionPool._connection_pool = self.mock_pool

    @patch('connection.pool.SimpleConnectionPool')
    def test_initialize_pool(self, mock_pool):
        DatabaseConnectionPool._connection_pool = None
        self.db_pool.initialize_pool(1, 10)
        mock_pool.assert_called_once_with(
            1, 10,
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        self.assertIsNotNone(DatabaseConnectionPool._connection_pool)

    @patch('connection.pool.SimpleConnectionPool')
    def test_initialize_pool_exception(self, mock_pool):
        mock_pool.side_effect = Exception("Failed to create connection pool")
        with self.assertRaises(Exception):
            DatabaseConnectionPool._connection_pool = None  # Ensure that _connection_pool is None to force initialization
            self.db_pool.initialize_pool(1, 10)

    def test_get_connection(self):
        mock_conn = MagicMock()
        self.mock_pool.getconn.return_value = mock_conn
        conn = self.db_pool.get_connection()
        self.assertEqual(conn, mock_conn)
        self.mock_pool.getconn.assert_called_once()

    def test_get_connection_exception(self):
        self.mock_pool.getconn.side_effect = Exception("Failed to get connection")
        with self.assertRaises(Exception):
            self.db_pool.get_connection()

    def test_get_connection_with_cursor(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        self.mock_pool.getconn.return_value = mock_conn
        conn, cursor = self.db_pool.get_connection_with_cursor()
        self.assertEqual(conn, mock_conn)
        self.assertEqual(cursor, mock_cursor)
        self.mock_pool.getconn.assert_called_once()

    def test_get_connection_with_cursor_exception(self):
        self.mock_pool.getconn.side_effect = Exception("Failed to get connection with cursor")
        with self.assertRaises(Exception):
            self.db_pool.get_connection_with_cursor()

    def test_put_connection(self):
        mock_conn = MagicMock()
        self.db_pool.put_connection(mock_conn)
        self.mock_pool.putconn.assert_called_once_with(mock_conn)

    def test_put_connection_exception(self):
        mock_conn = MagicMock()
        self.mock_pool.putconn.side_effect = Exception("Failed to put connection back to pool")
        with self.assertRaises(Exception):
            self.db_pool.put_connection(mock_conn)

    def test_close_all_connections(self):
        self.db_pool.close_all_connections()
        self.mock_pool.closeall.assert_called_once()

    def test_close_all_connections_exception(self):
        self.mock_pool.closeall.side_effect = Exception("Failed to close all connections")
        with self.assertRaises(Exception):
            self.db_pool.close_all_connections()

if __name__ == '__main__':
    unittest.main()
