from typing import List, Optional, Dict, Any
from datetime import datetime
from core.task import Task
from database.db_handler import MongoDBHandler


class TaskManager:
    """
    Manages task operations and business logic.
    """

    def __init__(self, db_handler: MongoDBHandler):
        """
        Initialize TaskManager with MongoDB handler.

        Args:
            db_handler: MongoDB handler instance
        """
        self.db_handler = db_handler

    def add_task(
        self,
        title: str,
        description: str = "",
        due_date: Optional[str] = None,
        priority: str = "Medium",
    ) -> bool:
        """
        Add a new task.

        Args:
            title: Task title
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Priority level

        Returns:
            bool: True if task was added successfully
        """
        try:
            # Validate inputs
            if not title.strip():
                raise ValueError("Task title cannot be empty")

            if due_date and not self._validate_date(due_date):
                raise ValueError("Invalid due date format. Use YYYY-MM-DD")

            if priority not in Task.PRIORITY_LEVELS:
                raise ValueError(f"Priority must be one of: {Task.PRIORITY_LEVELS}")

            # Create task
            task = Task(
                title=title.strip(),
                description=description.strip(),
                due_date=due_date,
                priority=priority,
            )

            # Save to database
            return self.db_handler.create_task(task.to_dict())

        except Exception as e:
            print(f"✗ Error adding task: {e}")
            return False

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks from MongoDB.

        Returns:
            List of Task objects
        """
        try:
            tasks_data = self.db_handler.get_all_tasks()
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"✗ Error retrieving tasks: {e}")
            return []

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object or None
        """
        try:
            task_data = self.db_handler.get_task_by_id(task_id)
            return Task.from_dict(task_data) if task_data else None
        except Exception as e:
            print(f"✗ Error retrieving task: {e}")
            return None

    def update_task(self, task_id: str, **updates) -> bool:
        """
        Update task details.

        Args:
            task_id: Task ID
            **updates: Fields to update

        Returns:
            bool: True if update was successful
        """
        try:
            # Check if task exists
            if not self.get_task_by_id(task_id):
                print("✗ Task not found")
                return False

            # Validate updates
            if (
                "due_date" in updates
                and updates["due_date"]
                and not self._validate_date(updates["due_date"])
            ):
                raise ValueError("Invalid due date format. Use YYYY-MM-DD")

            if (
                "priority" in updates
                and updates["priority"] not in Task.PRIORITY_LEVELS
            ):
                raise ValueError(f"Priority must be one of: {Task.PRIORITY_LEVELS}")

            if "status" in updates and updates["status"] not in Task.STATUS_OPTIONS:
                raise ValueError(f"Status must be one of: {Task.STATUS_OPTIONS}")

            return self.db_handler.update_task(task_id, updates)

        except Exception as e:
            print(f"✗ Error updating task: {e}")
            return False

    def mark_task_completed(self, task_id: str) -> bool:
        """
        Mark task as completed.

        Args:
            task_id: Task ID

        Returns:
            bool: True if task was marked as completed
        """
        return self.update_task(task_id, status="Completed")

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            bool: True if task was deleted
        """
        try:
            return self.db_handler.delete_task(task_id)
        except Exception as e:
            print(f"✗ Error deleting task: {e}")
            return False

    def search_tasks(self, search_term: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            search_term: Term to search for

        Returns:
            List of matching Task objects
        """
        try:
            tasks_data = self.db_handler.search_tasks(search_term)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"✗ Error searching tasks: {e}")
            return []

    def filter_tasks_by_status(self, status: str) -> List[Task]:
        """
        Filter tasks by status.

        Args:
            status: Status to filter by

        Returns:
            List of filtered Task objects
        """
        try:
            if status not in Task.STATUS_OPTIONS:
                raise ValueError(f"Status must be one of: {Task.STATUS_OPTIONS}")

            tasks_data = self.db_handler.filter_tasks_by_status(status)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"✗ Error filtering tasks: {e}")
            return []

    def sort_tasks(
        self, tasks: List[Task], sort_by: str = "created_at", reverse: bool = False
    ) -> List[Task]:
        """
        Sort tasks by specified criteria.

        Args:
            tasks: List of tasks to sort
            sort_by: Field to sort by
            reverse: Sort in descending order

        Returns:
            Sorted list of tasks
        """
        try:
            if sort_by == "priority":
                priority_order = {"High": 3, "Medium": 2, "Low": 1}
                return sorted(
                    tasks,
                    key=lambda t: priority_order.get(t.priority, 0),
                    reverse=reverse,
                )
            elif sort_by == "due_date":
                return sorted(
                    tasks, key=lambda t: t.due_date or "9999-12-31", reverse=reverse
                )
            elif sort_by == "title":
                return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
            else:  # created_at
                return sorted(tasks, key=lambda t: t.created_at, reverse=reverse)
        except Exception as e:
            print(f"✗ Error sorting tasks: {e}")
            return tasks

    def _validate_date(self, date_string: str) -> bool:
        """Validate date format YYYY-MM-DD."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def get_task_statistics(self) -> Dict[str, Any]:
        """Get task statistics."""
        try:
            tasks = self.get_all_tasks()
            total_tasks = len(tasks)

            if total_tasks == 0:
                return {
                    "total": 0,
                    "completed": 0,
                    "pending": 0,
                    "in_progress": 0,
                    "completion_rate": 0,
                }

            completed = len([t for t in tasks if t.status == "Completed"])
            pending = len([t for t in tasks if t.status == "Pending"])
            in_progress = len([t for t in tasks if t.status == "In Progress"])

            return {
                "total": total_tasks,
                "completed": completed,
                "pending": pending,
                "in_progress": in_progress,
                "completion_rate": round((completed / total_tasks) * 100, 2),
            }
        except Exception as e:
            print(f"✗ Error getting statistics: {e}")
            return {
                "total": 0,
                "completed": 0,
                "pending": 0,
                "in_progress": 0,
                "completion_rate": 0,
            }
