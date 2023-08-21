# Catalyst-Project

## Project Overview
Your task is to create a Web application using Django 3.x/4.x, Postgres and Bootstrap 4/5. <br> 
The application will allow users to login and upload a large volume data csv (1GB) with a visual progress of the upload. <br>
Once the file is uploaded, you must update the database with the contents of the file. <br>
Next, you must allow the user to filter the data using a form. Once the user submits the form, display the count of records based on the applied filters.

<br>
<br>

## Technology Used 
* Python 3.9.17
* Bootstrap - For the frontend pages
* django-all-auth - For user authentication
* Django REST API - For the file management
* Django Celery - For handling large datasets ( > ~ 1GB )
* Pandas for dataset operations
* django-environ - For securing configuration and secrets

## Initial Preparation
* Create python environment using Python 3.9.17
* Install requirement.txt : pip install -r requirement.txt
* Create .env file in "catalyst_count" folder with following fields : DEBUG ,SECRET_KEY ,DB_NAME , DB_USER , DB_PASSWORD , DB_HOST, DB_PORT
* Run django migrations
* Create super useer for login to access the file upload
* Open cmd in "catalyst_count" folder
* Start celery : celery -A catalyst_count worker -l info --pool=solo
  (As of now i am using in memory task queue . Further it can be configured with Redis or RabbitMQ)
* Start django application: python manage.py runserver

## Logics 
* catalyst/models.py contains the database models.
* catalyst/forms.py contains the forms for the user creation and query filter.
* catalyst/serializer.py contains the logic for exchanging json data from models like : User Model and Company Model
* catalyst/task.py contains the logic for cleaning the dataset and uploading the input file to the database. It does use the "celery" to do the task in asynchronous way. (Its very efficient to deal with large datasets.)
* catalyst/urls.py contains the routing logic.
* templates/account contains the html pages that are used in this project.

