from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import List, Optional
from datetime import datetime


class MongoDBHandler:
    """MongoDB database handler using pymongo."""

    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self) -> bool:
        """Establish MongoDB connection."""
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command("ping")

            self.db = self.client[self.database_name]
            self.collection = self.db.tasks

            # Create index on task_id for uniqueness
            self.collection.create_index("task_id", unique=True)

            print("Connected to MongoDB successfully")
            return True

        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            return False
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def create_task(self, task_data: dict) -> bool:
        """Create a new task in MongoDB."""
        try:
            task_data["created_at"] = datetime.now()
            task_data["updated_at"] = datetime.now()

            result = self.collection.insert_one(task_data)
            return result.inserted_id is not None

        except DuplicateKeyError:
            print("Task with this ID already exists")
            return False
        except Exception as e:
            print(f"Error creating task: {e}")
            return False

    def get_all_tasks(self) -> List[dict]:
        """Retrieve all tasks from MongoDB."""
        try:
            tasks = list(self.collection.find({}, {"_id": 0}).sort("created_at", -1))

            # Convert datetime objects to strings for JSON serialization
            for task in tasks:
                if task.get("created_at"):
                    task["created_at"] = task["created_at"].isoformat()
                if task.get("updated_at"):
                    task["updated_at"] = task["updated_at"].isoformat()
                if task.get("due_date") and isinstance(task["due_date"], datetime):
                    task["due_date"] = task["due_date"].isoformat()

            return tasks
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def get_task_by_id(self, task_id: str) -> Optional[dict]:
        """Get task by ID from MongoDB."""
        try:
            task = self.collection.find_one({"task_id": task_id}, {"_id": 0})

            if task:
                # Convert datetime objects to strings
                if task.get("created_at"):
                    task["created_at"] = task["created_at"].isoformat()
                if task.get("updated_at"):
                    task["updated_at"] = task["updated_at"].isoformat()
                if task.get("due_date") and isinstance(task["due_date"], datetime):
                    task["due_date"] = task["due_date"].isoformat()

            return task
        except Exception as e:
            print(f"✗ Error retrieving task: {e}")
            return None

    def update_task(self, task_id: str, updates: dict) -> bool:
        """Update task in MongoDB."""
        try:
            if not updates:
                return False

            # Add updated timestamp
            updates["updated_at"] = datetime.now()

            result = self.collection.update_one({"task_id": task_id}, {"$set": updates})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id: str) -> bool:
        """Delete task from MongoDB."""
        try:
            result = self.collection.delete_one({"task_id": task_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def search_tasks(self, search_term: str) -> List[dict]:
        """Search tasks by title or description."""
        try:
            query = {
                "$or": [
                    {"title": {"$regex": search_term, "$options": "i"}},
                    {"description": {"$regex": search_term, "$options": "i"}},
                ]
            }
            tasks = list(self.collection.find(query, {"_id": 0}).sort("created_at", -1))

            # Convert datetime objects to strings
            for task in tasks:
                if task.get("created_at"):
                    task["created_at"] = task["created_at"].isoformat()
                if task.get("updated_at"):
                    task["updated_at"] = task["updated_at"].isoformat()
                if task.get("due_date") and isinstance(task["due_date"], datetime):
                    task["due_date"] = task["due_date"].isoformat()

            return tasks
        except Exception as e:
            print(f"Error searching tasks: {e}")
            return []

    def filter_tasks_by_status(self, status: str) -> List[dict]:
        """Filter tasks by status."""
        try:
            tasks = list(
                self.collection.find({"status": status}, {"_id": 0}).sort(
                    "created_at", -1
                )
            )

            # Convert datetime objects to strings
            for task in tasks:
                if task.get("created_at"):
                    task["created_at"] = task["created_at"].isoformat()
                if task.get("updated_at"):
                    task["updated_at"] = task["updated_at"].isoformat()
                if task.get("due_date") and isinstance(task["due_date"], datetime):
                    task["due_date"] = task["due_date"].isoformat()

            return tasks
        except Exception as e:
            print(f"Error filtering tasks: {e}")
            return []

    def get_task_count(self) -> int:
        """Get total number of tasks."""
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting tasks: {e}")
            return 0

    def close_connection(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")
