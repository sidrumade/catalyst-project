# Catalyst-Project

## Project Overview
Your task is to create a Web application using Django 3.x/4.x, Postgres and Bootstrap 4/5. <br> 
The application will allow users to login and upload a large volume data csv (1GB) with a visual progress of the upload. <br>
Once the file is uploaded, you must update the database with the contents of the file. <br>
Next, you must allow the user to filter the data using a form. Once the user submits the form, display the count of records based on the applied filters.

<br>
<br>

### Initial Preparation
### Create python environment using Python 3.9.17
### install requirement.txt : pip install -r requirement.txt
### create .env file in "catalyst_count" folder with following fields :
#### DEBUG ,SECRET_KEY ,DB_NAME , DB_USER , DB_PASSWORD , DB_HOST, DB_PORT
### run django migrations
### Create super useer for login to access the file upload
### open cmd in "catalyst_count" folder
### start celery : celery -A catalyst_count worker -l info --pool=solo
### start django application: python manage.py runserver

