#!/bin/bash

# Run script for Linux/Mac - Starts the Flask application

echo -e "\033[32mStarting Flask application...\033[0m"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "\033[31mVirtual environment not found. Please run setup.sh first.\033[0m"
    exit 1
fi

# Activate virtual environment
echo -e "\033[33mActivating virtual environment...\033[0m"
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "\033[31mFailed to activate virtual environment\033[0m"
    exit 1
fi

# Run the Flask app
echo -e "\033[36mRunning Flask application on http://localhost:5000\033[0m"
python app.py
