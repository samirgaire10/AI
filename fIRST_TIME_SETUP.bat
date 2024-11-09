@echo off

echo starting service 
timeout /t 3 /nobreak > NUL

echo installing Flask
start cmd /c "pip install Flask"     

echo installing flask-cors
start cmd /c "pip install flask-cors"  

echo  beautifulsoup4
start cmd /c "pip install requests beautifulsoup4"  


start cmd /c "python app.py"
start cmd /c "python scripts/popular.py"
start php -S localhost:8000
timeout /t 1 /nobreak > NUL
start http://localhost:8000
