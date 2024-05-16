from models.dataAccess import DatabaseConnectionPool
from models.events import EventCreate, EventUpdate

async def get_event(event_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("SELECT * FROM events WHERE eventId = %s", (event_id,))
        event_record = cursor.fetchone()
        if event_record:
            columns = [col[0] for col in cursor.description]
            event_dict = {column: value for column, value in zip(columns, event_record)}
            return {
                'eventId': event_dict.get('eventid'),
                'eventName': event_dict.get('eventname'),
                'eventDescription': event_dict.get('eventdescription'),
                'userId': event_dict.get('userid'),
                'goalId': event_dict.get('goalid'),
                'isComplete': event_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def create_event(event: EventCreate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            INSERT INTO events (eventName, eventDescription, userId, goalId, isComplete)
            VALUES (%s, %s, %s, %s, %s) RETURNING *
            """, (event.eventName, event.eventDescription, event.userId, event.goalId, False))
        new_event = cursor.fetchone()
        conn.commit()
        if new_event:
            columns = [col[0] for col in cursor.description]
            new_event_dict = {column: value for column, value in zip(columns, new_event)}
            return {
                'eventId': new_event_dict.get('eventid'),
                'eventName': new_event_dict.get('eventname'),
                'eventDescription': new_event_dict.get('eventdescription'),
                'userId': new_event_dict.get('userid'),
                'goalId': new_event_dict.get('goalid'),
                'isComplete': new_event_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def update_event(event_id: int, event: EventUpdate):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("""
            UPDATE events SET eventName = %s, eventDescription = %s, isComplete = %s
            WHERE eventId = %s RETURNING *
            """, (event.eventName, event.eventDescription, event.isComplete, event_id))
        updated_event = cursor.fetchone()
        conn.commit()
        if updated_event:
            columns = [col[0] for col in cursor.description]
            updated_event_dict = {column: value for column, value in zip(columns, updated_event)}
            return {
                'eventId': updated_event_dict.get('eventid'),
                'eventName': updated_event_dict.get('eventname'),
                'eventDescription': updated_event_dict.get('eventdescription'),
                'userId': updated_event_dict.get('userid'),
                'goalId': updated_event_dict.get('goalid'),
                'isComplete': updated_event_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)

async def delete_event(event_id: int):
    conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
    try:
        cursor.execute("DELETE FROM events WHERE eventId = %s RETURNING *", (event_id,))
        deleted_event = cursor.fetchone()
        conn.commit()
        if deleted_event:
            columns = [col[0] for col in cursor.description]
            deleted_event_dict = {column: value for column, value in zip(columns, deleted_event)}
            return {
                'eventId': deleted_event_dict.get('eventid'),
                'eventName': deleted_event_dict.get('eventname'),
                'eventDescription': deleted_event_dict.get('eventdescription'),
                'userId': deleted_event_dict.get('userid'),
                'goalId': deleted_event_dict.get('goalid'),
                'isComplete': deleted_event_dict.get('iscomplete')
            }
        return None
    finally:
        cursor.close()
        DatabaseConnectionPool.put_connection(conn)
