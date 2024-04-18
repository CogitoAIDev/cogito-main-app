import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from connection import DatabaseConnectionPool

class UserPermanentContext:
    @staticmethod
    def validate_context(context):
        """
        Validate the context data against the required schema, ensuring all necessary fields are present and correctly formatted.
        """
        required_structures = {
            # add user backstory/description field
            # preffered voice tone (formal, informal, etc)
            "lifestylePreferences": ("preferredTimeOfDay", "activityType"),
            "motivationalTriggers": ("bestMotivators", "energyPeaks"),
            "personalNotes": None,  # This will just check for the presence of an empty list or initialized structure
            "updatedAt": None  # This expects a date, to be set upon creation
        }

        for key, subfields in required_structures.items():
            if key not in context:
                raise ValueError(f"Missing required field '{key}'.")
            if subfields is not None:
                if not isinstance(context[key], dict):
                    raise ValueError(f"The field '{key}' must be a dictionary.")
                for subfield in subfields:
                    if subfield not in context[key]:
                        raise ValueError(f"Missing subfield '{subfield}' in '{key}'.")
                    if not isinstance(context[key][subfield], (list if subfield.endswith('s') else str)):
                        raise ValueError(f"Subfield '{subfield}' in '{key}' must be {'a list' if subfield.endswith('s') else 'a string'}.")

    @staticmethod
    def create_context(user_id: int, context: dict):
        """
        Create a new user context and store it in the database after validating against the schema.
        """
        # Ensuring the updated date is set correctly upon creation
        context['updatedAt'] = datetime.now().isoformat()

        # Validating the context before inserting into the database
        UserPermanentContext.validate_context(context)

        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user_permanent_context (userId, context)
                VALUES (%s, %s)
                RETURNING contextId;
            """, (user_id, Json(context)))
            context_id = cursor.fetchone()[0]
            conn.commit()
            return context_id
        except Exception as e:
            print(f"Error creating user context: {e}")
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def update_context_detail(context_id, key, value):
        """
        Update a specific key within the user context JSONB structure.
        """
        # Handle datetime conversion
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, dict):
            value = {k: v.isoformat() if isinstance(v, datetime) else v for k, v in value.items()}

        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE user_permanent_context
                SET context = jsonb_set(context, %s, %s, true)
                WHERE contextId = %s;
            """, ('{' + key + '}', Json(value), context_id))
            conn.commit()
        except Exception as e:
            print(f"Error updating user context detail: {e}")
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def get_context_detail(context_id, key):
        """
        Retrieve a specific key from the context JSONB data.
        """
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT context -> %s FROM user_permanent_context WHERE contextId = %s;
            """, (key, context_id))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving user context detail: {e}")
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def delete_context_detail(context_id, key):
        """
        Delete a specific key from the context JSONB data.
        """
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE user_permanent_context
                SET context = context - %s
                WHERE contextId = %s;
            """, (key, context_id))
            conn.commit()
        except Exception as e:
            print(f"Error deleting user context detail: {e}")
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def get_context(context_id):
        """
        Retrieve the entire context JSONB data for a given context ID.
        """
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT context FROM user_permanent_context WHERE contextId = %s;
            """, (context_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving user context: {e}")
        finally:
            DatabaseConnectionPool.put_connection(conn)

    @staticmethod
    def delete_context(context_id):
        """
        Delete a user context from the database.
        """
        conn = DatabaseConnectionPool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM user_permanent_context WHERE contextId = %s;
            """, (context_id,))
            conn.commit()
        except Exception as e:
            print(f"Error deleting user context: {e}")
            conn.rollback()
        finally:
            DatabaseConnectionPool.put_connection(conn)

# Example usage
DatabaseConnectionPool.initialize_pool(minconn=1, maxconn=10)

# Create a new context with all required fields properly initialized
new_context = {
    "lifestylePreferences": {
        "preferredTimeOfDay": "morning",
        "activityType": "exercise"
    },
    "motivationalTriggers": {
        "bestMotivators": ["achievement", "collaboration"],
        "energyPeaks": ["morning", "afternoon"]
    },
    "personalNotes": [],  # Initially empty, can be populated later
    "updatedAt": datetime.now()  # Set the date when the context is created
}
user_id = 1  
context_id = UserPermanentContext.create_context(user_id, new_context)
print("New Context ID:", context_id)
print("---------------------------------")

# Get a specific context detail
print("Lifestyle Preferences:", UserPermanentContext.get_context_detail(context_id, 'lifestylePreferences'))
print("---------------------------------")
# Update a specific detail within the context
UserPermanentContext.update_context_detail(context_id, 'lifestylePreferences', {"preferredTimeOfDay": "evening", "activityType": "relaxation"})

# Fetch the updated context to see the changes
updated_context = UserPermanentContext.get_context(context_id)
print("Updated Context Data:", updated_context)
print("---------------------------------")
# Add a personal note
new_note = {
    "noteId": 1,  # This should be managed to ensure uniqueness
    "content": "First personal note",
    "date": datetime.now().isoformat()  # Timestamp for the note
}
UserPermanentContext.update_context_detail(context_id, 'personalNotes', [new_note])

# Fetch the updated context with the new note
updated_with_note = UserPermanentContext.get_context(context_id)
print("Updated Context with Note:", updated_with_note)
print("---------------------------------")
# Delete the entire context
UserPermanentContext.delete_context(context_id)
print("Context Deleted.")
print("---------------------------------")
