import psycopg2
from psycopg2.extras import Json
from datetime import datetime, date
from connection import DatabaseConnectionPool

class UserGoals:
    @staticmethod
    def create_goal(user_id: int, title: str, description: str, status: str, motivation_level: int, importance: str, due_date: date):
        # Validate inputs
        if not all([title, description, status, importance]) or not isinstance(motivation_level, int):
            raise ValueError("Missing or invalid input values.")

        # Check if the importance is one of the allowed values
        if importance not in ['Low', 'Medium', 'High']:
            raise ValueError("Importance must be 'Low', 'Medium', or 'High'.")

        # Ensure the status is a valid option
        if status not in ['pending', 'in progress', 'completed']:
            raise ValueError("Status must be 'pending', 'in progress', or 'completed'.")

        # Ensure the motivation level is within the correct range
        if not (1 <= motivation_level <= 10):
            raise ValueError("Motivation level must be between 1 and 10.")

        goal_details = {
            "title": title,
            "description": description,
            "status": status,
            "motivationLevel": motivation_level,
            "importance": importance,
            "dueDate": due_date.isoformat(),
            "createdDate": datetime.now().isoformat(),
            "updatedDate": datetime.now().isoformat(),
            "progressTracking": {
                "totalSteps": 0,
                "completedSteps": 0,
                "remainingSteps": 0
            },
            "reminders": []
        }
        return UserGoals.add_goal(user_id, goal_details)

    @staticmethod
    def add_goal(user_id: int, goal_details: dict):
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user_goals (userId, goalDetails) VALUES (%s, %s)
                RETURNING goalId;
            """, (user_id, Json(goal_details)))
            goal_id = cursor.fetchone()[0]
            conn.commit()
            return goal_id
        except Exception as e:
            print("Error adding new goal:", e)
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def update_goal_detail(goal_id, key, value):
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            # Update specific key value in the JSONB document
            cursor.execute("""
                UPDATE user_goals 
                SET goalDetails = jsonb_set(goalDetails, %s, %s, true)
                WHERE goalId = %s;
            """, ('{' + key + '}', Json(value), goal_id))
            conn.commit()
        except Exception as e:
            print("Error updating goal detail:", e)
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def get_goal_detail(goal_id, key):
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT goalDetails -> %s FROM user_goals WHERE goalId = %s;
            """, (key, goal_id))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print("Error fetching goal detail:", e)
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def delete_goal_detail(goal_id, key):
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            # Delete specific key from the JSONB document
            cursor.execute("""
                UPDATE user_goals
                SET goalDetails = goalDetails - %s
                WHERE goalId = %s;
            """, (key, goal_id))
            conn.commit()
        except Exception as e:
            print("Error deleting goal detail:", e)
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)
