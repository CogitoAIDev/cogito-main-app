from models.dataAccess import DatabaseConnectionPool
from models.messagesMetadata import MessageMetadataCreate, MessageMetadataUpdate

async def get_message_metadata(message_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("SELECT * FROM messages_metadata WHERE messageId = %s", (message_id,))
        message_record = cursor.fetchone()
        if message_record:
            columns = [col[0] for col in cursor.description]
            message_dict = {column: value for column, value in zip(columns, message_record)}
            return {
                'messageId': message_dict.get('messageid'),
                'sentTime': message_dict.get('senttime'),
                'userId': message_dict.get('userid'),
                'modelId': message_dict.get('modelid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def create_message_metadata(message: MessageMetadataCreate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            INSERT INTO messages_metadata (sentTime, userId, modelId)
            VALUES (%s, %s, %s) RETURNING *
            """, (message.sentTime, message.userId, message.modelId))
        new_message = cursor.fetchone()
        conn.commit()
        if new_message:
            columns = [col[0] for col in cursor.description]
            new_message_dict = {column: value for column, value in zip(columns, new_message)}
            return {
                'messageId': new_message_dict.get('messageid'),
                'sentTime': new_message_dict.get('senttime'),
                'userId': new_message_dict.get('userid'),
                'modelId': new_message_dict.get('modelid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def update_message_metadata(message_id: int, message: MessageMetadataUpdate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            UPDATE messages_metadata SET sentTime = %s, modelId = %s
            WHERE messageId = %s RETURNING *
            """, (message.sentTime, message.modelId, message_id))
        updated_message = cursor.fetchone()
        conn.commit()
        if updated_message:
            columns = [col[0] for col in cursor.description]
            updated_message_dict = {column: value for column, value in zip(columns, updated_message)}
            return {
                'messageId': updated_message_dict.get('messageid'),
                'sentTime': updated_message_dict.get('senttime'),
                'userId': updated_message_dict.get('userid'),
                'modelId': updated_message_dict.get('modelid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def delete_message_metadata(message_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("DELETE FROM messages_metadata WHERE messageId = %s RETURNING *", (message_id,))
        deleted_message = cursor.fetchone()
        conn.commit()
        if deleted_message:
            columns = [col[0] for col in cursor.description]
            deleted_message_dict = {column: value for column, value in zip(columns, deleted_message)}
            return {
                'messageId': deleted_message_dict.get('messageid'),
                'sentTime': deleted_message_dict.get('senttime'),
                'userId': deleted_message_dict.get('userid'),
                'modelId': deleted_message_dict.get('modelid')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)
