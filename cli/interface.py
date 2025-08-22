from typing import Optional
from core.task_manager import TaskManager
from core.task import Task


class TaskCLI:
    """
    Command-line interface for task management.
    """

    def __init__(self, task_manager: TaskManager):
        """
        Initialize CLI with task manager.

        Args:
            task_manager: TaskManager instance
        """
        self.task_manager = task_manager
        self.running = True

    def run(self):
        """Main CLI loop."""
        self.display_welcome()

        while self.running:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-7): ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    def display_welcome(self):
        """Display welcome message."""
        print("=" * 50)
        print("               NL TASK MANAGEMENT APP")
        print("=" * 50)
        print("Welcome! Manage your tasks efficiently.")
        print()

    def display_menu(self):
        """Display main menu options."""
        print("\n" + "-" * 30)
        print("           MAIN MENU")
        print("-" * 30)
        print("1. Add New Task")
        print("2. List All Tasks")
        print("3. Update Task")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. Filter Tasks")
        print("7. Exit")

    def handle_choice(self, choice: str):
        """Handle user menu choice."""
        handlers = {
            "1": self.add_task,
            "2": self.list_tasks,
            "3": self.update_task,
            "4": self.mark_completed,
            "5": self.delete_task,
            "6": self.filter_tasks,
            "7": self.exit_app,
        }

        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Invalid choice. Please enter a number between 1-7.")

    def add_task(self):
        """Add a new task through CLI."""
        print("\n--- ADD NEW TASK ---")

        try:
            title = input("Task Title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description = input("Description (optional): ").strip()
            due_date = input("Due Date (YYYY-MM-DD, optional): ").strip()

            print("Priority Levels: Low, Medium, High")
            priority = input("Priority (default: Medium): ").strip() or "Medium"

            if due_date == "":
                due_date = None

            if self.task_manager.add_task(title, description, due_date, priority):
                print("\n✓ Task added successfully!")
            else:
                print("\n✗ Failed to add task.")

        except Exception as e:
            print(f"Error adding task: {e}")

    def list_tasks(self):
        """List all tasks."""
        print("\n--- ALL TASKS ---")

        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        # Ask for sorting preference
        print("\nSort by:")
        print("  1) Created Date")
        print("  2) Priority")
        print("  3) Due Date")
        print("  4) Title")
        sort_choice = input("Choose sorting (default: 1): ").strip() or "1"

        sort_options = {
            "1": "created_at",
            "2": "priority",
            "3": "due_date",
            "4": "title",
        }

        sort_by = sort_options.get(sort_choice, "created_at")
        reverse = sort_choice == "2"  # High priority first

        sorted_tasks = self.task_manager.sort_tasks(tasks, sort_by, reverse)

        self.display_tasks(sorted_tasks)

        # Show statistics
        stats = self.task_manager.get_task_statistics()
        print("\n--- STATISTICS ---")
        print(f"Total Tasks    : {stats['total']}")
        print(f"Completed      : {stats['completed']}")
        print(f"Pending        : {stats['pending']}")
        print(f"In Progress    : {stats['in_progress']}")
        print(f"Completion Rate: {stats['completion_rate']}%")

    def update_task(self):
        """Update an existing task."""
        print("\n--- UPDATE TASK ---")

        task_id = self.get_task_id_input()
        if not task_id:
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print("Task not found.")
            return

        print("\nCurrent Task:")
        print(f"  Title      : {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Due Date   : {task.due_date or 'Not set'}")
        print(f"  Priority   : {task.priority}")
        print(f"  Status     : {task.status}")

        updates = {}

        # Get updates
        new_title = input(f"New Title (current: {task.title}): ").strip()
        if new_title:
            updates["title"] = new_title

        new_description = input(
            f"New Description (current: {task.description}): "
        ).strip()
        if new_description:
            updates["description"] = new_description

        new_due_date = input(
            f"New Due Date (current: {task.due_date or 'Not set'}): "
        ).strip()
        if new_due_date:
            updates["due_date"] = new_due_date

        print("Priority options: Low, Medium, High")
        new_priority = input(f"New Priority (current: {task.priority}): ").strip()
        if new_priority and new_priority in Task.PRIORITY_LEVELS:
            updates["priority"] = new_priority

        print("Status options: Pending, In Progress, Completed")
        new_status = input(f"New Status (current: {task.status}): ").strip()
        if new_status and new_status in Task.STATUS_OPTIONS:
            updates["status"] = new_status

        if updates:
            if self.task_manager.update_task(task_id, **updates):
                print("\n✓ Task updated successfully!")
            else:
                print("\n✗ Failed to update task.")
        else:
            print("\nNo changes made.")

    def mark_completed(self):
        """Mark a task as completed."""
        print("\n--- MARK TASK AS COMPLETED ---")

        task_id = self.get_task_id_input()
        if not task_id:
            return

        if self.task_manager.mark_task_completed(task_id):
            print("\n✓ Task marked as completed!")
        else:
            print("\n✗ Failed to mark task as completed.")

    def delete_task(self):
        """Delete a task."""
        print("\n--- DELETE TASK ---")

        task_id = self.get_task_id_input()
        if not task_id:
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print("Task not found.")
            return

        print(f"Task to delete: {task}")
        confirm = (
            input("Are you sure you want to delete this task? (y/N): ").strip().lower()
        )

        if confirm == "y":
            if self.task_manager.delete_task(task_id):
                print("\n✓ Task deleted successfully!")
            else:
                print("\n✗ Failed to delete task.")
        else:
            print("\nDelete cancelled.")

    def filter_tasks(self):
        """Filter and display tasks."""
        print("\n--- FILTER TASKS ---")

        print("Filter options (leave empty to skip):")
        status = input("Status (Pending/In Progress/Completed): ").strip() or None
        priority = input("Priority (Low/Medium/High): ").strip() or None
        due_date = input("Due Date (YYYY-MM-DD): ").strip() or None

        filtered_tasks = self.task_manager.filter_tasks(status, priority, due_date)

        if filtered_tasks:
            print(f"\n--- FILTERED RESULTS ({len(filtered_tasks)} tasks) ---")
            self.display_tasks(filtered_tasks)
        else:
            print("No tasks match the filter criteria.")

    def display_tasks(self, tasks):
        """Display a list of tasks in a formatted way."""
        if not tasks:
            print("No tasks to display.")
            return

        print(
            f"\n{'ID':<10} {'Title':<25} {'Status':<12} {'Priority':<8} {'Due Date':<12}"
        )
        print("-" * 75)

        for task in tasks:
            task_id_short = task.task_id[:8]
            title = task.title[:22] + "..." if len(task.title) > 25 else task.title
            due_date = task.due_date or "Not set"

            print(
                f"{task_id_short:<10} {title:<25} {task.status:<12} {task.priority:<8} {due_date:<12}"
            )

    def get_task_id_input(self) -> Optional[str]:
        """Get task ID from user input with validation."""
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks available.")
            return None

        print("\nAvailable tasks:")
        for task in tasks[:10]:  # Show first 10 tasks
            print(f"  {task.task_id[:8]} - {task.title}")

        if len(tasks) > 10:
            print(f"  ... and {len(tasks) - 10} more tasks")

        task_id_input = input(
            "\nEnter Task ID (first 8 characters are enough): "
        ).strip()

        if not task_id_input:
            print("Task ID cannot be empty.")
            return None

        # Find task by partial ID
        for task in tasks:
            if task.task_id.startswith(task_id_input):
                return task.task_id

        print("Task ID not found.")
        return None

    def exit_app(self):
        """Exit the application."""
        print("\nThank you for using Task Management Application!")
        print("Goodbye!")
        self.running = False
