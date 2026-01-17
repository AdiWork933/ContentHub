#!/bin/bash

# Setup script for Linux/Mac - Creates virtual environment and installs dependencies

echo -e "\033[32mSetting up Python virtual environment...\033[0m"

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
else
    OS="Unknown"
fi

echo -e "\033[33mDetected OS: $OS\033[0m"

# Check if venv already exists
if [ ! -d "venv" ]; then
    echo -e "\033[33mCreating virtual environment...\033[0m"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "\033[31mFailed to create virtual environment\033[0m"
        exit 1
    fi
else
    echo -e "\033[33mVirtual environment already exists\033[0m"
fi

# Activate virtual environment
echo -e "\033[33mActivating virtual environment...\033[0m"
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "\033[31mFailed to activate virtual environment\033[0m"
    exit 1
fi

# Install requirements
echo -e "\033[33mInstalling requirements...\033[0m"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "\033[31mFailed to install requirements\033[0m"
    exit 1
fi

echo -e "\033[32mSetup completed successfully!\033[0m"
echo -e "\033[36mVirtual environment is activated. You can now run the project.\033[0m"
