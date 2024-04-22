import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from connection import DatabaseConnectionPool
from contextlib import contextmanager

class UserGoalsDB:
    @staticmethod
    @contextmanager
    def get_db_cursor():
        conn, cursor = DatabaseConnectionPool.get_connection_with_cursor()
        try:
            yield cursor
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error: {e}")
        else:
            conn.commit()
        finally:
            cursor.close()
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def create_goal(user_id: int, goal_data: dict):
        UserGoalsValidator.validate_goal_data(user_id, goal_data)
        goal_data['createdDate'] = datetime.now().isoformat()
        goal_data['updatedDate'] = datetime.now().isoformat()
        goal_data.setdefault('progressTracking', {"totalSteps": 0, "completedSteps": 0, "skippedSteps": 0})

        with UserGoalsDB.get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_goals (userId, goalDetails) VALUES (%s, %s) RETURNING goalId;
            """, (user_id, Json(goal_data)))
            goal_id = cursor.fetchone()[0]
            return goal_id

    @staticmethod
    def update_goal_detail(goal_id, key, value):
        UserGoalsValidator.validate_key_value(key, value)
        with UserGoalsDB.get_db_cursor() as cursor:
            json_path = f"{{{key}}}"
            json_value = Json(value)
            cursor.execute("""
                UPDATE user_goals
                SET goalDetails = jsonb_set(goalDetails, %s::text[], %s, true)
                WHERE goalId = %s;
            """, ([json_path], json_value, goal_id))

    @staticmethod
    def get_goal_detail(goal_id, key):
        with UserGoalsDB.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT goalDetails -> %s FROM user_goals WHERE goalId = %s;
            """, (key, goal_id))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def delete_goal_detail(goal_id, key):
        with UserGoalsDB.get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE user_goals
                SET goalDetails = goalDetails - %s
                WHERE goalId = %s;
            """, (key, goal_id))


class UserGoalsValidator:
    @staticmethod
    def validate_goal_data(user_id, goal_data):
        if not isinstance(user_id, int):
            raise ValueError("User ID must be an integer.")
        UserGoalsValidator.validate_goal_details(goal_data)
        UserGoalsValidator.validate_progress_tracking(goal_data)

    @staticmethod
    def validate_goal_details(goal_data):
        goal_details_required_fields = {
            "title": str,
            "description": str,
            "status": str,
            "motivationLevel": int,
            "importance": str,
            "dueDate": str,
            "overviewStatement": str
        }
        goal_data['goalDetails'] = goal_data.get('goalDetails', {})
        UserGoalsValidator.validate_section(goal_data['goalDetails'], goal_details_required_fields)
        UserGoalsValidator.validate_status(goal_data['goalDetails'])
        UserGoalsValidator.validate_motivation_level(goal_data['goalDetails'])
        UserGoalsValidator.validate_importance(goal_data['goalDetails'])
        UserGoalsValidator.validate_due_date(goal_data['goalDetails'])

    @staticmethod
    def validate_progress_tracking(goal_data):
        progress_tracking_required_fields = {
            "totalSteps": int,
            "completedSteps": int,
            "skippedSteps": int
        }
        goal_data['progressTracking'] = goal_data.get('progressTracking', {})
        UserGoalsValidator.validate_section(goal_data['progressTracking'], progress_tracking_required_fields)

    @staticmethod
    def validate_section(section, required_fields):
        for key, expected_type in required_fields.items():
            if key not in section:
                section[key] = [] if expected_type is list else (0 if expected_type is int else ('' if expected_type is str else False))
            elif not isinstance(section[key], expected_type):
                raise ValueError(f"'{key}' in 'goalDetails' must be {expected_type.__name__}.")

    @staticmethod
    def validate_status(goal_details):
        if goal_details.get('status') not in ['Pending', 'In Progress', 'Completed']:
            raise ValueError("Invalid status. Must be 'Pending', 'In Progress', or 'Completed'.")

    @staticmethod
    def validate_motivation_level(goal_details):
        if not isinstance(goal_details.get('motivationLevel'), int) or not 1 <= goal_details.get('motivationLevel') <= 10:
            raise ValueError("Motivation level must be an integer between 1 and 10.")

    @staticmethod
    def validate_importance(goal_details):
        if goal_details.get('importance') not in ['Low', 'Medium', 'High']:
            raise ValueError("Invalid importance. Must be 'Low', 'Medium', or 'High'.")

    @staticmethod
    def validate_due_date(goal_details):
        try:
            datetime.strptime(goal_details.get('dueDate'), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid due date. Must be in 'YYYY-MM-DD' format.")

    @staticmethod
    def validate_key_value(key, value):
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        if key == 'status' and value not in ['Pending', 'In Progress', 'Completed']:
            raise ValueError("Invalid status. Must be 'Pending', 'In Progress', or 'Completed'.")
        if key == 'motivationLevel' and (not isinstance(value, int) or not 1 <= value <= 10):
            raise ValueError("Motivation level must be an integer between 1 and 10.")
        if key == 'importance' and value not in ['Low', 'Medium', 'High']:
            raise ValueError("Invalid importance. Must be 'Low', 'Medium', or 'High'.")
        if key == 'dueDate':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid due date. Must be in 'YYYY-MM-DD' format.")
        if key in ['totalSteps', 'completedSteps', 'skippedSteps'] and not isinstance(value, int):
            raise ValueError(f"{key.capitalize()} must be an integer.")