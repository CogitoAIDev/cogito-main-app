# UserGoals Class Documentation

The `UserGoals` class in Python provides structured management for user goals stored in a PostgreSQL database using the JSONB data type. This class enables creating, updating, retrieving, and deleting details of goals, ensuring adherence to a predefined schema and facilitating robust data handling.

## Dependencies

This class uses the `psycopg2` package for PostgreSQL interactions, managed through a connection pool for efficient connection handling.

Ensure the necessary package is installed:

    pip install psycopg2

## Module: `user_goals.py`

This module handles operations related to user goals, such as creating new goals, updating details within a goal, retrieving specific goal details, and deleting details.

### Class Methods Overview

#### create_goal
Constructs and validates a goal's details before passing the data to `add_goal` for insertion into the database.

##### Parameters
- `user_id (int)`: Identifier of the user to whom the goal belongs.
- `title (str)`: Title of the goal.
- `description (str)`: Detailed description of the goal.
- `status (str)`: Current status of the goal (valid values: 'pending', 'in progress', 'completed').
- `motivation_level (int)`: Motivation level, rated between 1 and 10.
- `importance (str)`: Importance of the goal (valid values: 'Low', 'Medium', 'High').
- `due_date (date)`: Target completion date for the goal.

##### Returns
- `int`: Unique identifier of the created goal.

#### add_goal
Inserts a new goal into the database using details prepared by `create_goal`.

##### Parameters
- `user_id (int)`: User's identifier.
- `goal_details (dict)`: Structured dictionary containing details about the goal.

##### Returns
- `int`: Goal ID from the database after successful insertion.

##### Usage
```python
    goal_details = {
        "title": "Complete Python Course",
        "description": "Finish all chapters of Python mastery",
        "status": "in progress",
        "motivationLevel": 7,
        "importance": "High",
        "dueDate": "2023-12-31T00:00:00",
        "createdDate": "2023-01-01T00:00:00",
        "updatedDate": "2023-01-01T00:00:00",
        "progressTracking": {
            "totalSteps": 10,
            "completedSteps": 0,
            "remainingSteps": 10
        },
        "reminders": []
    }
    goal_id = UserGoals.add_goal(1, goal_details)
```
#### update_goal_detail
Modifies a specific key within the goal's JSONB structure in the database.

##### Parameters
- `goal_id (int)`: Identifier of the goal.
- `key (str)`: Key within the JSONB data to update.
- `value (varies)`: New value for the specified key.

##### Usage
```python
    UserGoals.update_goal_detail(1, "motivationLevel", 9)
```
#### get_goal_detail
Retrieves a particular detail from a goal's JSONB structure based on the provided key.

##### Parameters
- `goal_id (int)`: Identifier for the goal.
- `key (str)`: Key whose value is to be retrieved.

##### Returns
- `varies`: Value of the specified key from the JSONB data.

##### Usage
```python
    status = UserGoals.get_goal_detail(1, "status")
```
#### delete_goal_detail
Removes a specific key from a goal's JSONB structure.

##### Parameters
- `goal_id (int)`: Identifier for the goal.
- `key (str)`: Key to be removed from the JSONB data.

##### Usage
```
    UserGoals.delete_goal_detail(1, "importance")
```
## Conclusion

The `UserGoals` class effectively manages user goals within a PostgreSQL database using JSONB. It ensures data integrity and allows for complex data manipulation, providing a flexible yet structured approach to goal management. Proper utilization of this class supports maintaining business rules and data standards across the application.
