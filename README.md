# TASK-MANAGEMENT-CLI

A command-line task management application built with Python and MongoDB.

## Features

- ✅ Add, update, delete, and list tasks
- ✅ Filter tasks by status, priority, or due date
- ✅ Sort tasks by various criteria
- ✅ Mark tasks as completed
- ✅ Task statistics and completion tracking
- ✅ MongoDB database support
- ✅ Input validation and error handling

## Installation (Windows)

### 1. Clone the Repository

```bash
git clone https://github.com/cromcruach52/TASK-MANAGEMENT-CLI.git
```

### 2. Install MongoDB

- Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
- Run the installer and follow the setup wizard
- MongoDB will run as a Windows service automatically

### 3. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install pymongo
pip install pymongo
```

### 4. Configure and Run

```bash
# Set up database
python scripts/setup_database.py

# Run the application
python main.py
```

## Usage

Run `python main.py` and use the interactive menu to manage your tasks.

## Requirements

- Python 3.7+
- MongoDB Community Server
- pymongo library

