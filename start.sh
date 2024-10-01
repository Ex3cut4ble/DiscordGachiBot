#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$DIR/venv"
PYTHON_VENV="$VENV_DIR/bin/python"

if [ -d "$VENV_DIR" ]; then
    echo "Venv found."
else
    echo "Venv not found, creating one..."
    python -m venv "$VENV_DIR"

    if [ -f "$PYTHON_VENV" ]; then
        echo "Venv successfully created."
    else
        echo "Error occured while creating venv. Exiting..."
        exit 1
    fi

    source "$VENV_DIR/bin/activate"
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$DIR/requirements.txt"
    deactivate

    if [ $? -ne 0 ]; then
        echo "Error occured while installing dependencies. Exiting..."
        deactivate
        exit 1
    fi
fi

source "$VENV_DIR/bin/activate"
echo "Starting bot..."
python "$DIR/main.py"

echo "Bot stopped."
deactivate