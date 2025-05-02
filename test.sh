#!/bin/bash

# CONFIGURATION
LINTING="false"
TYPE_CHECKING="false"
SECURITY_CHECKING="false"
CLEANUP="true"

# Step 1: Build the project
echo "Starting the build process..."
bash build.sh
if [ $? -ne 0 ]; then
    echo "Build failed. Exiting."
    exit 1
fi
echo "Build completed successfully."

# Step 2: Install dependencies
echo "Installing test dependencies..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip. Exiting."
    exit 1
fi

python3 -m pip install -r test/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    exit 1
fi
echo "Dependencies installed successfully."

# Step 3: Run unit tests
echo "Running unit tests..."
python3 test/test.py
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Exiting."
    exit 1
fi
echo "Unit tests passed successfully."

# Step 4: Run linting
if [ "$LINTING" = "true" ]; then
    echo "Running lint checks..."
    python3 -m pip install flake8
    if [ $? -ne 0 ]; then
        echo "Failed to install flake8. Exiting."
        exit 1
    fi

    flake8 .
    if [ $? -ne 0 ]; then
        echo "Linting failed. Please fix the issues."
        exit 1
    fi
    echo "Linting passed successfully."
fi    

# Step 5: Run type checks
if [ "$TYPE_CHECKING" = "true" ]; then
    echo "Running type checks with mypy..."
    python3 -m pip install mypy
    if [ $? -ne 0 ]; then
        echo "Failed to install mypy. Exiting."
        exit 1
    fi

    mypy .
    if [ $? -ne 0 ]; then
        echo "Type checks failed. Please fix the issues."
        exit 1
    fi
    echo "Type checks passed successfully."
fi

# Step 6: Run security checks
if [ "$SECURITY_CHECKING" = "true" ]; then
    echo "Running security checks with bandit..."
    python3 -m pip install bandit
    if [ $? -ne 0 ]; then
        echo "Failed to install bandit. Exiting."
        exit 1
    fi

    bandit -r .
    if [ $? -ne 0 ]; then
        echo "Security checks failed. Please fix the issues."
        exit 1
    fi
    echo "Security checks passed successfully."
fi

# Step 7: Clean up temporary files
if [ "$CLEANUP" = "true" ]; then
    echo "Cleaning up temporary files..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -r {} +
    echo "Cleanup completed."
fi

# Final message
echo "All steps completed successfully."