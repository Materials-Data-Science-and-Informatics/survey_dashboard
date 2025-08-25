#!/bin/bash

# Function to create new Poetry environment and store path
create_new_poetry_env() {
    echo "Creating new Poetry environment..."
    
    # Install dependencies and get the virtual environment path
    poetry install
    
    # Get the virtual environment path
    POETRY_ENV_PATH=$(poetry env info --path)
    
    if [ -z "$POETRY_ENV_PATH" ]; then
        echo "Error: Could not determine Poetry environment path"
        exit 1
    fi
    
    # Store the path in .env file
    echo "POETRY_ENV_PATH=$POETRY_ENV_PATH" > .env
    echo "Stored Poetry environment path in .env file: $POETRY_ENV_PATH"
    
    # Activate the environment
    source "$POETRY_ENV_PATH/bin/activate"
}

# Activate Poetry environment and run the survey dashboard in development mode
export PATH="$HOME/.local/bin:$PATH"

# Check if .env file exists and contains POETRY_ENV_PATH
if [ -f ".env" ] && grep -q "POETRY_ENV_PATH" .env; then
    # Load environment variables from .env file
    export $(cat .env | grep -v '^#' | xargs)
    
    # Check if the stored path still exists
    if [ -d "$POETRY_ENV_PATH" ]; then
        echo "Using existing Poetry environment: $POETRY_ENV_PATH"
        source "$POETRY_ENV_PATH/bin/activate"
    else
        echo "Stored Poetry environment not found, creating new one..."
        rm .env  # Remove invalid .env file
        create_new_poetry_env
    fi
else
    echo "No .env file found, creating new Poetry environment..."
    create_new_poetry_env
fi

# Run the panel server
echo "Starting Survey Dashboard on http://localhost:5006/"
echo "Press Ctrl+C to stop the server"
panel serve --port 5006 survey_dashboard/ 