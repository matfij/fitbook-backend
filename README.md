# FitBook backend
Python Django Rest Framework Application

## Virtual environment
 - activation: `.venv\Scripts\activate`
 - installing dependencies: `pip3 install -r requirements.txt`

## Docker
 - build image: `docker build .`
 - compose: `docker-compose build`
 - run api: `docker-compose run api sh -c "[target command]"`
 - run tests: `docker-compose run api sh -c "python3 manage.py test && flake8"`

## Migrations
 - migrate: `docker-compose run api sh -c "python3 manage.py makemigrations [project_name]"`
