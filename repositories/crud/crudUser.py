from models.dataAccess import DatabaseConnectionPool
from models.users import UserCreate, UserUpdate

async def get_user(user_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE userId = %s", (user_id,))
        user_record = cursor.fetchone()
        if user_record:
            columns = [col[0] for col in cursor.description]
            user_dict = {column: value for column, value in zip(columns, user_record)}
            return {
                'userId': user_dict.get('userid'),
                'userName': user_dict.get('username'),
                'telegramChatId': user_dict.get('telegramchatid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def create_user(user: UserCreate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("INSERT INTO users (userName, telegramChatId) VALUES (%s, %s) RETURNING *",
                       (user.userName, user.telegramChatId))
        new_user = cursor.fetchone()
        conn.commit()
        if new_user:
            columns = [col[0] for col in cursor.description]
            new_user_dict = {column: value for column, value in zip(columns, new_user)}
            return {
                'userId': new_user_dict.get('userid'),
                'userName': new_user_dict.get('username'),
                'telegramChatId': new_user_dict.get('telegramchatid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def update_user(user_id: int, user: UserUpdate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        # First fetch the existing user to retrieve the `telegramChatId`
        cursor.execute("SELECT telegramChatId FROM users WHERE userId = %s", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            return None  # User not found, can't update

        # Update user name (telegramChatId is not updated)
        cursor.execute("UPDATE users SET userName = %s WHERE userId = %s RETURNING *",
                       (user.userName, user_id))
        updated_user = cursor.fetchone()
        conn.commit()

        if updated_user:
            columns = [col[0] for col in cursor.description]
            updated_user_dict = {column: value for column, value in zip(columns, updated_user)}
            return {
                'userId': updated_user_dict.get('userid'),
                'userName': updated_user_dict.get('username'),
                'telegramChatId': existing_user[0]  # Use existing telegramChatId
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def delete_user(user_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("DELETE FROM users WHERE userId = %s RETURNING *", (user_id,))
        deleted_user = cursor.fetchone()
        conn.commit()
        if deleted_user:
            columns = [col[0] for col in cursor.description]
            deleted_user_dict = {column: value for column, value in zip(columns, deleted_user)}
            return {
                'userId': deleted_user_dict.get('userid'),
                'userName': deleted_user_dict.get('username'),
                'telegramChatId': deleted_user_dict.get('telegramchatid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)
