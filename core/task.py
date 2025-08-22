from datetime import datetime
from typing import Optional
import uuid


class Task:
    """
    Represents a single task with all its attributes.
    """

    PRIORITY_LEVELS = ["Low", "Medium", "High"]
    STATUS_OPTIONS = ["Pending", "In Progress", "Completed"]

    def __init__(
        self,
        title: str,
        description: str = "",
        due_date: Optional[str] = None,
        priority: str = "Medium",
        status: str = "Pending",
        task_id: Optional[str] = None,
    ):
        """
        Initialize a new task.

        Args:
            title (str): Task title
            description (str): Task description
            due_date (str, optional): Due date in YYYY-MM-DD format
            priority (str): Priority level (Low, Medium, High)
            status (str): Task status (Pending, In Progress, Completed)
            task_id (str, optional): Unique task ID (auto-generated if not provided)
        """
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority if priority in self.PRIORITY_LEVELS else "Medium"
        self.status = status if status in self.STATUS_OPTIONS else "Pending"
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert task to dictionary for database storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task instance from dictionary."""
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending"),
            task_id=data.get("task_id"),
        )
        task.created_at = data.get("created_at", datetime.now().isoformat())
        return task

    def update(self, **kwargs):
        """Update task attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == "priority" and value not in self.PRIORITY_LEVELS:
                    continue
                if key == "status" and value not in self.STATUS_OPTIONS:
                    continue
                setattr(self, key, value)

    def mark_completed(self):
        """Mark task as completed."""
        self.status = "Completed"

    def __str__(self) -> str:
        """String representation of the task."""
        return f"[{self.task_id[:8]}] {self.title} - {self.status} ({self.priority})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"Task(id={self.task_id[:8]}, title='{self.title}', status='{self.status}')"
        )
