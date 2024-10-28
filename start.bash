#!/bin/bash

# Start app.py in the background
python app.py &

# Start updatemodels.py in the background
python scripts/updatemodels.py &

# Start the PHP server
php -S localhost:8000 &

# Wait for a few seconds
sleep 5

# Open the default web browser
xdg-open http://localhost:8000  # For Linux
# open http://localhost:8000      # For macOS
# start http://localhost:8000      # For Windows (in WSL)
