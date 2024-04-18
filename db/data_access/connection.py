import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnectionPool:
    _connection_pool = None

    @staticmethod
    def initialize_pool(minconn, maxconn):
        if DatabaseConnectionPool._connection_pool is None:
            DatabaseConnectionPool._connection_pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'cogitotest1'),
                user=os.getenv('DB_USER', 'procrastinatormuffin'),
                password=os.getenv('DB_PASSWORD', 'D213141516171d'),
                port=os.getenv('DB_PORT', '5432') 
            )
            print("Connection pool created")

    @staticmethod
    def get_connection():
        if DatabaseConnectionPool._connection_pool is None:
            raise Exception("Database connection pool is not initialized")
        return DatabaseConnectionPool._connection_pool.getconn()

    @staticmethod
    def put_connection(conn):
        DatabaseConnectionPool._connection_pool.putconn(conn)

    @staticmethod
    def close_all_connections():
        if DatabaseConnectionPool._connection_pool:
            DatabaseConnectionPool._connection_pool.closeall()
            print("Connection pool closed")
