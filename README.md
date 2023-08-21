# catalyst-project
### Initial Preparation
### Create python environment using Python 3.9.17
### install requirement.txt : pip install -r requirement.txt
### create .env file in "catalyst_count" folder with following fields :
#### DEBUG ,SECRET_KEY ,DB_NAME , DB_USER , DB_PASSWORD , DB_HOST, DB_PORT
### run django migrations
### open cmd in "catalyst_count" folder
### start celery : celery -A catalyst_count worker -l info --pool=solo
### start django application: python manage.py runserver

