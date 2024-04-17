# Database Connection Pool Documentation

The `DatabaseConnectionPool` class provides a centralized mechanism for managing PostgreSQL database connections using a connection pool. This document outlines how to utilize this class within the Python codebase.

## Module: `connection.py`

This module initializes and manages a connection pool for PostgreSQL database connections, facilitating efficient reuse and management of connections throughout the application.

### Dependencies

Before using the module, ensure the following Python package is installed:

- `psycopg2`: PostgreSQL database adapter for Python
- `python-dotenv`: Loads environment variables from a `.env` file

Install these packages using pip if not already installed:

    pip install psycopg2 python-dotenv

### Environment Configuration

The database connection parameters are managed via environment variables. These variables should be set in a `.env` file located at the root of the project. Here is an example of the contents of the `.env` file:

    DB_HOST=localhost
    DB_NAME=myapp_db
    DB_USER=myapp_user
    DB_PASSWORD=myapp_secure_password
    DB_PORT=5432

### Class `DatabaseConnectionPool`

#### Initialization
```python
    @staticmethod
    def initialize_pool(minconn, maxconn):
        """
        Initialize the database connection pool.

        Args:
        - minconn (int): Minimum number of connections in the pool.
        - maxconn (int): Maximum number of connections in the pool.

        Environment Variables:
        - DB_HOST: Database host address.
        - DB_NAME: Database name.
        - DB_USER: Database user.
        - DB_PASSWORD: Database password.
        - DB_PORT: Database port.

        Raises:
        - Exception: If the connection pool is already initialized.
        """
        if DatabaseConnectionPool._connection_pool is None:
            DatabaseConnectionPool._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'your_database'),
                user=os.getenv('DB_USER', 'your_user'),
                password=os.getenv('DB_PASSWORD', 'your_password'),
                port=os.getenv('DB_PORT', '5432')
            )
            print("Connection pool created")
        else:
            raise Exception("Connection pool is already initialized")
```
#### Get Connection
```python
    @staticmethod
    def get_connection():
        """
        Retrieve a connection from the connection pool.

        Returns:
        - Connection object from psycopg2.

        Raises:
        - Exception: If the connection pool is not initialized.
        """
        if DatabaseConnectionPool._connection_pool is None:
            raise Exception("Database connection pool is not initialized")
        return DatabaseConnectionPool._connection_pool.getconn()
```
#### Release Connection
```python
    @staticmethod
    def put_connection(conn):
        """
        Return a connection back to the connection pool.

        Args:
        - conn: The connection object to be returned.

        Raises:
        - Exception: If the connection object is None.
        """
        if conn is not None:
            DatabaseConnectionPool._connection_pool.putconn(conn)
        else:
            raise Exception("No connection provided")
```
#### Close All Connections
```python
    @staticmethod
    def close_all_connections():
        """
        Close all connections in the pool and shut down the pool.
        """
        if DatabaseConnectionPool._connection_pool:
            DatabaseConnectionPool._connection_pool.closeall()
            print("Connection pool closed")
```
### Example Usage
```python
    from db.connection import DatabaseConnectionPool

    # Initialize connection pool
    DatabaseConnectionPool.initialize_pool(minconn=1, maxconn=10)

    # Get a connection from the pool
    conn = DatabaseConnectionPool.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print(rows)
    finally:
        # Always return the connection to the pool
        DatabaseConnectionPool.put_connection(conn)

    # Close all connections on application shutdown
    DatabaseConnectionPool.close_all_connections()
```
## Conclusion

This module is designed to efficiently manage database connections using pooling to optimize resource usage and performance in high-load environments. Proper initialization, usage, and teardown of the connection pool are crucial for the stable operation of applications relying on database interactions.
