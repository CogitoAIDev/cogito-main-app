from models.dataAccess import DatabaseConnectionPool
from models.notifications import NotificationCreate, NotificationUpdate

async def get_notification(notification_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("SELECT * FROM notifications WHERE notificationId = %s", (notification_id,))
        notification_record = cursor.fetchone()
        if notification_record:
            columns = [col[0] for col in cursor.description]
            notification_dict = {column: value for column, value in zip(columns, notification_record)}
            return {
                'notificationId': notification_dict.get('notificationid'),
                'eventId': notification_dict.get('eventid'),
                'time': notification_dict.get('time'),
                'isComplete': notification_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def create_notification(notification: NotificationCreate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            INSERT INTO notifications (eventId, time, isComplete)
            VALUES (%s, %s, %s) RETURNING *
            """, (notification.eventId, notification.time, False))
        new_notification = cursor.fetchone()
        conn.commit()
        if new_notification:
            columns = [col[0] for col in cursor.description]
            new_notification_dict = {column: value for column, value in zip(columns, new_notification)}
            return {
                'notificationId': new_notification_dict.get('notificationid'),
                'eventId': new_notification_dict.get('eventid'),
                'time': new_notification_dict.get('time'),
                'isComplete': new_notification_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def update_notification(notification_id: int, notification: NotificationUpdate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            UPDATE notifications SET time = %s, isComplete = %s
            WHERE notificationId = %s RETURNING *
            """, (notification.time, notification.isComplete, notification_id))
        updated_notification = cursor.fetchone()
        conn.commit()
        if updated_notification:
            columns = [col[0] for col in cursor.description]
            updated_notification_dict = {column: value for column, value in zip(columns, updated_notification)}
            return {
                'notificationId': updated_notification_dict.get('notificationid'),
                'eventId': updated_notification_dict.get('eventid'),
                'time': updated_notification_dict.get('time'),
                'isComplete': updated_notification_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def delete_notification(notification_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("DELETE FROM notifications WHERE notificationId = %s RETURNING *", (notification_id,))
        deleted_notification = cursor.fetchone()
        conn.commit()
        if deleted_notification:
            columns = [col[0] for col in cursor.description]
            deleted_notification_dict = {column: value for column, value in zip(columns, deleted_notification)}
            return {
                'notificationId': deleted_notification_dict.get('notificationid'),
                'eventId': deleted_notification_dict.get('eventid'),
                'time': deleted_notification_dict.get('time'),
                'isComplete': deleted_notification_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)
