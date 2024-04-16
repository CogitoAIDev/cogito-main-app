import psycopg2 # type: ignore
import random
from datetime import datetime, timedelta
import json
from faker import Faker # type: ignore

fake = Faker()

conn = psycopg2.connect(
    dbname="cogitotest", 
    user="postgres", # Replace this with your PostgreSQL username
    password="pass", # Replace this with your PostgreSQL password
    host="localhost", 
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()

for _ in range(10000, 100000):
    cursor.execute(
        "INSERT INTO users (userName, userTelegramId) VALUES (%s, %s)",
        (fake.name(), fake.urandom_int(min=100000000, max=999999999))
    )

model_sizes = [128, 256, 512]
for i in range(1, 21): 
    cursor.execute(
        "INSERT INTO models (modelName, modelSize) VALUES (%s, %s)",
        (f"Model_{i}", random.choice(model_sizes))
    )

cursor.execute("SELECT userId FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT modelId FROM models")
model_ids = [row[0] for row in cursor.fetchall()]

for user_id in user_ids:
    goal_details_json = json.dumps({"details": fake.text()})
    cursor.execute(
        "INSERT INTO user_goals (userId, goalDetails) VALUES (%s, %s)",
        (user_id, goal_details_json)
    )

cursor.execute("SELECT goalId FROM user_goals")
goal_ids = [row[0] for row in cursor.fetchall()]

for user_id in user_ids:
    goal_id = random.choice(goal_ids)
    cursor.execute(
        "INSERT INTO events (eventName, userId, goalId, isComplete) VALUES (%s, %s, %s, %s)",
        (fake.word(), user_id, goal_id, random.choice([True, False]))
    )

cursor.execute("SELECT eventId FROM events")
event_ids = [row[0] for row in cursor.fetchall()]

for event_id in event_ids:
    cursor.execute(
        "INSERT INTO notifications (eventId, time, isComplete) VALUES (%s, %s, %s)",
        (event_id, fake.date_time_between(start_date="-1y", end_date="now"), random.choice([True, False]))
    )

for user_id in user_ids:
    model_id = random.choice(model_ids)
    cursor.execute(
        "INSERT INTO messages_metadata (sentTime, userId, modelId) VALUES (%s, %s, %s)",
        (fake.date_time_between(start_date="-1y", end_date="now"), user_id, model_id)
    )

for user_id in user_ids:
    context_json = json.dumps({"context": fake.text()})
    cursor.execute(
        "INSERT INTO user_permanent_context (userId, context) VALUES (%s, %s)",
        (user_id, context_json)
    )

for user_id in user_ids:
    report_json = json.dumps({"report": fake.sentence()})
    cursor.execute(
        "INSERT INTO daily_reports (reportDate, userId, report) VALUES (%s, %s, %s)",
        (datetime.now() - timedelta(days=random.randint(0, 365)), user_id, report_json)
    )

cursor.close()
conn.close()

print("Data generation complete.")
