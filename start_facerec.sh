#!/bin/bash

# Function to wait for the X server
wait_for_x() {
    while ! xset q &>/dev/null; do
        echo "Waiting for X server..."
        sleep 1
    done
}

# Navigate to the Flask application directory
cd flask_app

# Activate the virtual environment
source ./venv/bin/activate

# Start the Flask application
python3 app.py &

# Wait for the X server to be ready
wait_for_x

# Wait for a few more seconds to ensure the Flask app is running
sleep 10

# Clear Chromium browser cache
#rm -rf ~/.config/chromium/Default

# Launch Chromium browser in full-screen mode with flags to disable session restore prompt
chromium-browser --start-fullscreen --disable-session-crashed-bubble --disable-infobars --incognito --disable-restore-session-state http://localhost:5000/face_recognition/facerec__

