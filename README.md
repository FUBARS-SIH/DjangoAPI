# DjangoAPI
The Django backend API endpoints for the app.

# Setup

## Postgres installation (for development environment)

- Follow the instructions [here](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
- Database details
  - Name: mdm
  - User: mdm_user
  - Password: InchOwiL

## Python packages required

- `django`, `psycopg2`, `virtualenv`

## Using the project

- Make and run migrations:
  ```bash
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```
- Run server:
  ```bash
  $ python manage.py runserver
  ```
- Open browser and access the website on [127.0.0.1:8000](http://127.0.0.1:8000)
