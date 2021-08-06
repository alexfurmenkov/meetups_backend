## Meetups project

The project is a small backend app. The idea: users can create meetups that are held at a certain time and place. 
The meetup can be educational, sport or professional.

### Features
* Signup
* Login
* Retrieve all users or a single user
* Update/Delete a user
* Create a new meetup
* Retrieve all meetups or a single meetup
* Update/Delete a meetup

### Stack
* Programming language - Python
* Web Framework - Django
* DB - PostgreSQL

### Launching the project

1. Create a Postgres DB called "meetups_db" on your computer.
2. Run `python3 -m venv venv` to create a virtual environment.
3. Run `source venv/bin/activate` to activate a virtual environment.
4. Run `pip install -r requirements.txt` to install all necessary dependencies.
5. Run `python src/manage.py makemigrations meetups_backend` to create migrations.
6. Run `python src/manage.py migrate` to apply the migrations.
7. Run `python src/manage.py loaddata --app meetups_backend post_type.json` to populate the DB with the post types.
8. Run `python src/manage.py runserver localhost:8000` to launch the server.

### Launching the project using Docker

The project can also be launched using Docker. It will create two containers: the app itself and a Postgres DB. 
Besides launching the containers, you also have to apply migrations and populate the DB with the post types.

1. Run `docker-compose up -d` to create and launch backend and DB containers.
2. Run `docker-compose exec backend python /code/manage.py makemigrations meetups_backend` to create migrations.
3. Run `docker-compose exec backend python /code/manage.py migrate` to apply the migrations.
4. Run `docker-compose exec backend python /code/manage.py loaddata --app meetups_backend post_type.json` to populate the DB with the post types.

### Running automated tests

Simply execute `python src/manage.py test tests`.

**A more detailed documentation can be found in "docs" directory. 
It describes the API endpoints, DB schema, migrations and automated tests.** 

### Further plans
In the future, I would like to implement the following features:
* Reset password
* Assign a user to a certain meetup
* Remind the user about the meetup via email notification