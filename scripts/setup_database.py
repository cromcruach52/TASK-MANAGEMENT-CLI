"""
Database setup script for creating tables and initial data.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_config import DatabaseConfig
from database.db_handler import MongoDBHandler


def setup_mongodb():
    """
    Set up MongoDB database and test connection.

    Returns:
        bool: True if setup successful, False otherwise
    """
    print("Setting up MongoDB database...")

    try:
        config = DatabaseConfig.get_mongodb_config()
        handler = MongoDBHandler(config["connection_string"], config["database_name"])

        if handler.connect():
            print("✓ MongoDB connection successful!")
            print("✓ Database ready for use!")
            handler.close_connection()
            return True
        else:
            print("✗ Failed to connect to MongoDB")
            return False

    except Exception as e:
        print(f"MongoDB setup error: {e}")
        return False


def main():
    """
    Main setup function that initializes the database.

    Tests MongoDB connection and prepares the database for use.
    """
    print("Database Setup Script")
    print("=" * 30)

    print("Database type: MONGODB")

    success = setup_mongodb()

    if success:
        print("\n✓ Database setup completed successfully!")
        print("You can now run the main application: python main.py")
    else:
        print("\n✗ Database setup failed!")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
