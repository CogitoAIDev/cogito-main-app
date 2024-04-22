import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnectionPool:
    _connection_pool = None

    @classmethod
    def initialize_pool(cls, minconn, maxconn):
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pool.SimpleConnectionPool(
                    minconn,
                    maxconn,
                    host=os.getenv('DB_HOST'),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    port=os.getenv('DB_PORT') 
                )
                print("Connection pool created")
            except Exception as e:
                print(f"Failed to create connection pool: {e}")
                raise

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            raise Exception("Database connection pool is not initialized")
        try:
            return cls._connection_pool.getconn()
        except Exception as e:
            print(f"Failed to get connection: {e}")
            raise

    @classmethod
    def get_connection_with_cursor(cls):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            print(f"Failed to get connection with cursor: {e}")
            raise

    @classmethod
    def put_connection(cls, conn):
        try:
            cls._connection_pool.putconn(conn)
        except Exception as e:
            print(f"Failed to put connection back to pool: {e}")
            raise

    @classmethod
    def close_all_connections(cls):
        if cls._connection_pool:
            try:
                cls._connection_pool.closeall()
                print("Connection pool closed")
            except Exception as e:
                print(f"Failed to close all connections: {e}")
                raise