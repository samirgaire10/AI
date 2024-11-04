#!/bin/bash

python app.py &
python scripts/updatemodels.py &

php -S localhost:8000 &
sleep 3

xdg-open http://localhost:8000  # For Linux
# open http://localhost:8000      # For macOS
# start http://localhost:8000      # For Windows (in WSL)
