import os
from typing import Dict, Any


class DatabaseConfig:
    """Database configuration management."""

    @staticmethod
    def get_mongodb_config() -> Dict[str, Any]:
        """Get MongoDB configuration from environment variables."""
        return {
            "connection_string": os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
            "database_name": os.getenv("DB_NAME", "task_manager"),
        }


# Environment variable template
ENV_TEMPLATE = """
# Database Configuration
DATABASE_TYPE=mongodb

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DB_NAME=task_manager
"""
