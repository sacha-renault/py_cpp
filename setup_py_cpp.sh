#!/bin/bash

# Define the alias name and the command to run your Python script
ALIAS_NAME="py_cpp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/py_cpp.py"

# Check if the alias already exists in bashrc
if grep -Fxq "alias $ALIAS_NAME=" ~/.bashrc
then
    echo "Alias $ALIAS_NAME already exists in ~/.bashrc"
else
    # Append the alias to ~/.bashrc
    echo "alias $ALIAS_NAME='python3 $SCRIPT_PATH'" >> ~/.bashrc
    echo "Alias $ALIAS_NAME added to ~/.bashrc"
fi

# Source the updated ~/.bashrc
source ~/.bashrc

echo "Script setup complete. You can now use the alias '$ALIAS_NAME' to run your script."