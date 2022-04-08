# SK_P12

This application use Python 3.9.

## BACKEND
### Create virtual environment and install all dependencies

Below, the command lines steps to follow to install local API.

Check python version :   
`python --version`

Check if "venv" exist :   
`python -m venv --help`

If necessary, point other drive (example for "e" letter)  
`cd /d e:`

Define the root project directory :  
Example :   
`cd E:\DOCUMENTS\PROJETS\EpicEvents`

Create virtual environment who use Python 3.9 :    
`py -3.9 -m venv env`

Start virtual environment :     
`call  env/Scripts/activate.bat`

Install packages from requirements file :   
`pip install -r requirements.txt`

(If you want write requierements file, use this commande line)  
`pip freeze > requirements.txt`

Go to in "src" directory with :  
`cd src`

Run backend server :  
`python manage.py runserver`

API documentation :  
link

### Install psql and create a database
Download and install the latest postgresql version :  
https://www.postgresql.org/download/  
(postgresql-14.1-1-windows-x64.exe)

On Windows, add psql to environment variables Path :  
`C:\Program Files\PostgreSQL\14\bin`

Launch psql and use defaults credentials (defines during installation):    
`psql -U postgres`

Create a new user password :   
`CREATE USER yourusername WITH ENCRYPTED PASSWORD 'yourpassword';`

Show users list :  
`\du`

Show all databases :  
`\l`

To change language into user interface :  
`SET lc_messages TO 'en_US.UTF-8`

Create database with owner :  
`CREATE DATABASE "epicevents" WITH OWNER "yourusername";`

Remove database :  
`DROP DATABASE epicevents;`

Grant access to user :  
`GRANT ALL PRIVILEGES ON DATABASE epicevents TO yourusername;`

Add Create DB role :  
`ALTER USER yourusername CREATEDB;`

Connect to a database with "postgres" :    
`\c epicevents`

(Connect to a database with "yourusername")  
`psql -U yourusername  epicevents`

Show relations :    
`\dt`

(Remove table)  
`DROP TABLE clients_client CASCADE;`


### Secret key and database credentials

Before push your commits to git, make you surer than SECRET_KEY is not visible. 
To generate a new key:  
- run Python interpreter with `python manage.py shell`
- import get_rand_secret_key function `from django.core.management.utils import get_random_secret_key` 
- generate a new key `get_random_secret_key()`
- close shell `exit()`

Steps to deploy your key and set database credentials:  
First, create a ".env" file in "src" directory.
In this file :
- add a line with your custom key :  
`SECRET_KEY=myCustomKey`
- add those lines to connect your a Django project to the database:  
`DB_NAME=epicevents`  
`DB_USER=yourusername`  
`DB_PASSWORD=yourpassword.`  
`DB_HOST=localhost`  
`DB_PORT=5432`

- to finish, in settings.py file, import dotenv `from dotenv import load_dotenv`, replace your secret key by `str(os.getenv('SECRET_KEY'))` and load your key with `load_dotenv()`
