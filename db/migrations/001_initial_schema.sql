CREATE TABLE users (
    userId SERIAL PRIMARY KEY,
    userName VARCHAR NOT NULL,
    userTelegramId VARCHAR UNIQUE
);


CREATE TABLE events (
    eventId SERIAL PRIMARY KEY ,
    eventName VARCHAR NOT NULL,
    userId SERIAL NOT NULL,
    goalId SERIAL,
    isComplete BOOLEAN NOT NULL DEFAULT false
);


CREATE TABLE notifications (
    notificationId SERIAL PRIMARY KEY,
    eventId SERIAL NOT NULL,
    time TIMESTAMP NOT NULL,
    isComplete BOOLEAN NOT NULL DEFAULT false
);


CREATE TABLE messages_metadata (
    messageId SERIAL PRIMARY KEY,
    sentTime TIMESTAMP NOT NULL,
    userId SERIAL NOT NULL,
    modelId SERIAL
);


CREATE TABLE models (
    modelId SERIAL PRIMARY KEY,
    modelName VARCHAR NOT NULL UNIQUE,
    modelSize INT NOT NULL
);


CREATE TABLE user_goals (
    goalId SERIAL PRIMARY KEY,
    userId SERIAL NOT NULL,
    goalDetails JSONB NOT NULL
);


CREATE TABLE user_permanent_context (
    contextId SERIAL PRIMARY KEY,
    userId SERIAL NOT NULL,
    context JSONB NOT NULL
);


CREATE TABLE daily_reports (
    reportId SERIAL PRIMARY KEY,
    reportDate TIMESTAMP NOT NULL,
    userId SERIAL NOT NULL,
    report JSONB NOT NULL
);


-- Adding foreign keys
-- Foreign keys for events table
ALTER TABLE events ADD FOREIGN KEY (userId) REFERENCES users (userId);
ALTER TABLE events ADD FOREIGN KEY (goalId) REFERENCES user_goals (goalId);
-- Foreign key for notification table
ALTER TABLE notifications ADD FOREIGN KEY (eventId) REFERENCES events (eventId);
-- Foreign keys for messages_metadata table
ALTER TABLE messages_metadata ADD FOREIGN KEY (userId) REFERENCES users (userId);
ALTER TABLE messages_metadata ADD FOREIGN KEY (modelId) REFERENCES models (modelId);
-- Foreign key for user_goals table
ALTER TABLE user_goals ADD FOREIGN KEY (userId) REFERENCES users (userId);
-- Foreign key for user_permanent_context table
ALTER TABLE user_permanent_context ADD FOREIGN KEY (userId) REFERENCES users (userId);
-- Foreign key for daily_reports table
ALTER TABLE daily_reports ADD FOREIGN KEY (userId) REFERENCES users (userId);



-- Adding indexes
CREATE INDEX idx_events_userId ON events USING btree (userId);
CREATE INDEX idx_events_goalId ON events USING btree (goalId);
CREATE INDEX idx_notifications_eventId ON notifications USING btree (eventId);
CREATE INDEX idx_user_goals_userId ON user_goals USING btree (userId);
