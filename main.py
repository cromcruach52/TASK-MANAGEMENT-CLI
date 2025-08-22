import sys
import os
from typing import Optional


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_config import DatabaseConfig
from database.db_handler import MongoDBHandler
from core.task_manager import TaskManager
from cli.interface import TaskCLI


def create_database_handler() -> Optional[MongoDBHandler]:
    try:
        print("Initializing MongoDB connection...")
        config = DatabaseConfig.get_mongodb_config()

        handler = MongoDBHandler(
            connection_string=config["connection_string"],
            database_name=config["database_name"],
        )

        # Test connection
        if handler.connect():
            print("✓ Connected to MongoDB successfully!")
            return handler
        else:
            print("✗ Failed to connect to MongoDB")
            return None

    except ImportError as e:
        print(f"Missing required database library: {e}")
        print("Please install the required dependencies:")
        print("  pip install pymongo")
        return None
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def main():
    """Main application function."""
    print("Starting Task Management Application...")

    # Create database handler
    db_handler = create_database_handler()
    if not db_handler:
        print("Failed to initialize database connection.")
        print("Please check your database configuration and try again.")
        sys.exit(1)

    try:
        # Create task manager
        task_manager = TaskManager(db_handler)

        # Create and run CLI
        cli = TaskCLI(task_manager)
        cli.run()

    except Exception as e:
        print(f"Application error: {e}")
    finally:
        # Clean up database connection
        if db_handler:
            db_handler.close_connection()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
