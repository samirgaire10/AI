@echo off
start cmd /c "app.py"
start cmd /c "scripts\updatemodels.py"
start php -S localhost:8000
timeout /t 5 /nobreak > NUL
start http://localhost:8000