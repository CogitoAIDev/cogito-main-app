import psycopg2
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
import statistics

def connect_db():
    return psycopg2.connect(
        dbname="cogitotest", 
        user="postgres", # Replace this with your PostgreSQL username
        password="pass", # Replace this with your PostgreSQL password
        host="localhost", 
        port="5432"
    )

def db_operation(cursor, operation_type):
    start_time = time.time()
    try:
        if operation_type == "read_user":
            cursor.execute("SELECT * FROM users ORDER BY random() LIMIT 1")
        elif operation_type == "read_event":
            cursor.execute("SELECT * FROM events ORDER BY random() LIMIT 1")
        elif operation_type == "update_event":
            new_status = random.choice([True, False])
            cursor.execute("UPDATE events SET isComplete = %s WHERE eventId = (SELECT eventId FROM events ORDER BY random() LIMIT 1) RETURNING eventId", (new_status,))
        elif operation_type == "insert_notification":
            cursor.execute("INSERT INTO notifications (eventId, time, isComplete) VALUES ((SELECT eventId FROM events ORDER BY random() LIMIT 1), %s, %s) RETURNING notificationId", (datetime.now(), False))
        result = cursor.fetchall()
    except Exception as e:
        return (operation_type, 0, time.time() - start_time, str(e))
    return (operation_type, 1, time.time() - start_time, result)

def simulate_user_activity(user_id):
    with connect_db() as conn:
        with conn.cursor() as cursor:
            operations = ["read_user", "read_event", "update_event", "insert_notification"]
            results = []
            for _ in range(10):  # Each user performs 10 operations
                operation_type = random.choice(operations)
                result = db_operation(cursor, operation_type)
                results.append(result)
    return results

def main():
    num_users = 500
    operation_stats = {op: [] for op in ["read_user", "read_event", "update_event", "insert_notification"]}
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(simulate_user_activity, user_id) for user_id in range(num_users)]
        for future in as_completed(futures):
            for operation_type, success, duration, result in future.result():
                operation_stats[operation_type].append((duration, success))

    # Output statistics
    for operation, durations in operation_stats.items():
        if durations:
            durations_only = [d for d, s in durations if s]
            print(f"Stats for {operation}:")
            print(f"  Avg Time: {statistics.mean(durations_only):.4f} s")
            print(f"  Med Time: {statistics.median(durations_only):.4f} s")
            print(f"  Max Time: {max(durations_only):.4f} s")
            print(f"  Min Time: {min(durations_only):.4f} s")
            print(f"  Success Rate: {sum(1 for _, s in durations if s) / len(durations):.2%}")

if __name__ == "__main__":
    main()