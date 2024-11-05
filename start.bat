@echo off

echo starting service 
timeout /t 3 /nobreak > NUL

start cmd /c "app.py"
start cmd /c "scripts/updatemodels.py"
start php -S localhost:8000
timeout /t 1 /nobreak > NUL
start http://localhost:8000
