import psycopg2
import random
from datetime import datetime, timedelta
import json
from faker import Faker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

fake = Faker()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
conn.autocommit = True
cursor = conn.cursor()

# Set to keep track of used Telegram Chat IDs
used_telegram_ids = set()

user_data = []
for _ in range(100000):
    while True:
        potential_id = fake.random_int(min=100000000, max=999999999)
        if potential_id not in used_telegram_ids:
            used_telegram_ids.add(potential_id)
            break
    user_data.append((fake.name(), potential_id))

cursor.executemany(
    "INSERT INTO users (userName, telegramChatId) VALUES (%s, %s)",
    user_data
)

model_sizes = [128, 256, 512]
models_data = [(f"Model_{i}", random.choice(model_sizes)) for i in range(1, 21)]
cursor.executemany(
    "INSERT INTO models (modelName, modelSize) VALUES (%s, %s)",
    models_data
)

cursor.execute("SELECT userId FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT modelId FROM models")
model_ids = [row[0] for row in cursor.fetchall()]

goal_data = [(user_id, json.dumps({"details": fake.text()})) for user_id in user_ids]
cursor.executemany(
    "INSERT INTO user_goals (userId, goalDetails, isActive) VALUES (%s, %s, %s)",
    [(user_id, goal_details, random.choice([True, False])) for user_id, goal_details in goal_data]
)

cursor.execute("SELECT goalId FROM user_goals")
goal_ids = [row[0] for row in cursor.fetchall()]

events_data = [
    (fake.word(), user_id, random.choice(goal_ids), random.choice([True, False]))
    for user_id in user_ids
]
cursor.executemany(
    "INSERT INTO events (eventName, eventDescription, userId, goalId, isComplete) VALUES (%s, %s, %s, %s, %s)",
    [(event_name, fake.sentence(), user_id, goal_id, is_complete) for event_name, user_id, goal_id, is_complete in events_data]
)

cursor.execute("SELECT eventId FROM events")
event_ids = [row[0] for row in cursor.fetchall()]

notifications_data = [
    (event_id, fake.date_time_between(start_date="-1y", end_date="now"), random.choice([True, False]))
    for event_id in event_ids
]
cursor.executemany(
    "INSERT INTO notifications (eventId, time, isComplete) VALUES (%s, %s, %s)",
    notifications_data
)

max_message_id_query = "SELECT COALESCE(MAX(messageId), 0) FROM messages_metadata"
cursor.execute(max_message_id_query)
max_message_id = cursor.fetchone()[0]

messages_data = [
    (max_message_id + i + 1, fake.date_time_between(start_date="-1y", end_date="now"), user_id, random.choice(model_ids))
    for i, user_id in enumerate(user_ids)
]
cursor.executemany(
    "INSERT INTO messages_metadata (messageId, sentTime, userId, modelId) VALUES (%s, %s, %s, %s)",
    messages_data
)

context_data = [
    (user_id, json.dumps({"context": fake.text()}))
    for user_id in user_ids
]
cursor.executemany(
    "INSERT INTO user_context (userId, context) VALUES (%s, %s)",
    context_data
)

report_data = [
    (datetime.now() - timedelta(days=random.randint(0, 365)), user_id, json.dumps({"report": fake.sentence()}))
    for user_id in user_ids
]
cursor.executemany(
    "INSERT INTO daily_reports (reportDate, userId, report) VALUES (%s, %s, %s)",
    report_data
)

cursor.close()
conn.close()

print("Data generation complete.")
