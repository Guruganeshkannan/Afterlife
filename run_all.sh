#!/bin/bash
echo "Starting After Life Message Platform..."

# Start the backend server in a new terminal
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "python run_backend.py"'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    gnome-terminal -- bash -c "python run_backend.py; exec bash"
else
    echo "Unsupported operating system for automatic terminal opening"
    echo "Please run 'python run_backend.py' in a separate terminal"
fi

# Wait a moment for the backend to start
sleep 5

# Start the frontend server in a new terminal
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "python run_frontend.py"'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    gnome-terminal -- bash -c "python run_frontend.py; exec bash"
else
    echo "Unsupported operating system for automatic terminal opening"
    echo "Please run 'python run_frontend.py' in a separate terminal"
fi

echo "Servers are starting in separate terminals."
echo "Backend will be available at http://localhost:8000"
echo "Frontend will be available at http://localhost:3000" 