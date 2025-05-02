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
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip. Exiting."
    exit 1
fi

python -m pip install -r test/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Exiting."
    exit 1
fi
echo "Dependencies installed successfully."

# Step 3: Run unit tests
echo "Running unit tests..."
python test/test.py
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Exiting."
    exit 1
fi
echo "Unit tests passed successfully."

# Step 4: Run linting
echo "Running lint checks..."
python -m pip install flake8
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

# Step 5: Run type checks
echo "Running type checks with mypy..."
python -m pip install mypy
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

# Step 6: Run security checks
echo "Running security checks with bandit..."
python -m pip install bandit
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

# Step 7: Clean up temporary files
echo "Cleaning up temporary files..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +
echo "Cleanup completed."

# Final message
echo "All steps completed successfully."