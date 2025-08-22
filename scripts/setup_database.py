import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_config import DatabaseConfig
from database.db_handler import PostgreSQLHandler, MongoDBHandler


def setup_postgresql():
    """Set up PostgreSQL database and tables."""
    print("Setting up PostgreSQL database...")

    try:
        config = DatabaseConfig.get_postgresql_config()
        handler = PostgreSQLHandler(config)

        if handler.connect():
            print("✓ PostgreSQL connection successful!")
            print("✓ Tables created successfully!")
            handler.close_connection()
            return True
        else:
            print("✗ Failed to connect to PostgreSQL")
            return False

    except Exception as e:
        print(f"PostgreSQL setup error: {e}")
        return False


def setup_mongodb():
    """Set up MongoDB database."""
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
    """Main setup function."""
    print("Database Setup Script")
    print("=" * 30)

    db_type = DatabaseConfig.get_database_type()
    print(f"Database type: {db_type.upper()}")

    if db_type == "postgresql":
        success = setup_postgresql()
    elif db_type == "mongodb":
        success = setup_mongodb()
    else:
        print(f"Unsupported database type: {db_type}")
        success = False

    if success:
        print("\n✓ Database setup completed successfully!")
        print("You can now run the main application: python main.py")
    else:
        print("\n✗ Database setup failed!")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
