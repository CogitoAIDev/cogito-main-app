import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from .connection import DatabaseConnectionPool
from contextlib import contextmanager

class UserContextDB:
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
    def create_context(user_id: int, context: dict):
        UserContextValidator.validate_context(context)
        context['updatedAt'] = datetime.now().isoformat()

        with UserContextDB.get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_permanent_context (userId, context) VALUES (%s, %s) RETURNING contextId;
            """, (user_id, Json(context)))
            context_id = cursor.fetchone()[0]
            return context_id

    @staticmethod
    def update_context_detail(context_id, key, value):
        with UserContextDB.get_db_cursor() as cursor:
            json_path = f"{{{key}}}"
            json_value = Json(value)
            cursor.execute("""
                UPDATE user_permanent_context
                SET context = jsonb_set(context, %s::text[], %s, true)
                WHERE contextId = %s;
            """, ([json_path], json_value, context_id))

    @staticmethod
    def get_context_detail(context_id, key):
        with UserContextDB.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT context -> %s FROM user_permanent_context WHERE contextId = %s;
            """, (key, context_id))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def delete_context_detail(context_id, key):
        with UserContextDB.get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE user_permanent_context
                SET context = context - %s
                WHERE contextId = %s;
            """, (key, context_id))

    @staticmethod
    def get_context(context_id):
        with UserContextDB.get_db_cursor() as cursor:
            cursor.execute("""
                SELECT context FROM user_permanent_context WHERE contextId = %s;
            """, (context_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def delete_context(context_id):
        with UserContextDB.get_db_cursor() as cursor:
            cursor.execute("""
                DELETE FROM user_permanent_context WHERE contextId = %s;
            """, (context_id,))


class UserContextValidator:
    @staticmethod
    def validate_context(context):
        context['updatedAt'] = datetime.now().isoformat() if not isinstance(context.get('updatedAt'), str) else context['updatedAt']
        UserContextValidator.validate_permanent_section(context)
        UserContextValidator.validate_temporal_section(context)
        context['updatedAt'] = datetime.now().isoformat()

    @staticmethod
    def validate_permanent_section(context):
        permanent_required_fields = {
            "userBackstory": str,
            "lifestylePreferences": list,
            "motivationalTriggers": list,
            "preferredTone": str
        }
        context['permanent'] = context.get('permanent', {})
        UserContextValidator.validate_section(context['permanent'], permanent_required_fields)
        UserContextValidator.validate_lifestyle_preferences(context['permanent'])
        UserContextValidator.validate_motivational_triggers(context['permanent'])

    @staticmethod
    def validate_temporal_section(context):
        temporal_required_fields = {
            "userMood": str,
            "moodRelevance": bool,
            "lastMessageDate": str,
            "lastMessageCount": int,
            "lastMessageHistory": list
        }
        context['temporal'] = context.get('temporal', {})
        UserContextValidator.validate_section(context['temporal'], temporal_required_fields)
        UserContextValidator.validate_last_message_history(context['temporal'])

    @staticmethod
    def validate_section(section, required_fields):
        for key, expected_type in required_fields.items():
            if key not in section:
                section[key] = [] if expected_type is list else (0 if expected_type is int else ('' if expected_type is str else False))
            elif not isinstance(section[key], expected_type):
                raise ValueError(f"'{key}' in 'permanent' must be {expected_type.__name__}.")

    @staticmethod
    def validate_lifestyle_preferences(permanent):
        if permanent.get('lifestylePreferences'):
            for pref in permanent['lifestylePreferences']:
                if not all(k in pref for k in ['preferenceId', 'preferredTimeOfDay', 'activityType']):
                    raise ValueError("Each item in 'lifestylePreferences' must contain 'preferenceId', 'preferredTimeOfDay', and 'activityType'.")

    @staticmethod
    def validate_motivational_triggers(permanent):
        if permanent.get('motivationalTriggers'):
            for trig in permanent['motivationalTriggers']:
                if not all(k in trig for k in ['triggerId', 'motivationalFactor']):
                    raise ValueError("Each item in 'motivationalTriggers' must contain 'triggerId' and 'motivationalFactor'.")

    @staticmethod
    def validate_last_message_history(temporal):
        if temporal.get('lastMessageHistory'):
            for message in temporal['lastMessageHistory']:
                if not all(k in message for k in ['messageId', 'content', 'date']):
                    raise ValueError("Each item in 'lastMessageHistory' must contain 'messageId', 'content', and 'date'.")
