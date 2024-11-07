@echo off

echo starting service 
timeout /t 3 /nobreak > NUL

start cmd /c "python app.py"
start cmd /c "python scripts/popular.py"
start php -S localhost:8000
timeout /t 1 /nobreak > NUL
start http://localhost:8000
