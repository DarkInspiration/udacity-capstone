# Casting Agency App

Full - Stack Developer Nanodegree Program capstone project

# Motivation

We wanted to create an app where you can get a list of actors and movies, add new, modify or even delete actors and movies - based on your role and permissions in the agency. 

Heroku link:
```http: // udacity - casting - agency - capston.herokuapp.com/```

# Getting Started

# Installing Dependencies

# Python 3.7

Follow instructions to install the latest version of python for your platform in the[python docs](https: // docs.python.org / 3 / using / unix.html  # getting-and-installing-the-latest-version-of-python)

# Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https: // packaging.python.org / guides / installing - using - pip - and-virtual - environments /)

# PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/ backend` directory and running:

```bash
pip install - r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

# Key Dependencies

- [Flask](http: // flask.pocoo.org /)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https: // www.sqlalchemy.org /) and [Flask-SQLAlchemy](https: // flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https: // python - jose.readthedocs.io / en / latest /) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

# Creating DB
Postgress server is needed for database.

```createdb casting_agency```

then run

```flask db upgrade```

to execute DB upgrades from migration files

# Running the server

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=debug
flask run - -reload
```

App is accessed on:

```
http: // 0.0.0.0: 8080 /
```

# Running the tests
Inside ```auth / test_env.py``` you can set JWT tokens for each given role, the tokens will be used to run the tests.

To run the tests, execute:

```bash
python3 test_app.py
```

delete: movie
# Roles

Casting Assistant

- GET: actors
- GET: movies

Casting Director
# All permissions a Casting Assistant has
- POST: actor
- DELETE: actor
- PATCH: actors
- PATCH: movies

Executive Producer

# All permissions a Casting Director has
- POST: movies
- DELETE: movie

# Endpoints

# Possible Endpoints
```
GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
DELETE '/actors/[actor_id]'
DELETE '/movies/[movie_id]'
PATCH '/actors/[actor_id]'
PATCH '/movies/[movie_id]'
```

# Possible errors
```
{"error": 400, "message": "Bad request"}
{"error": 401, "message": "Unauthorized"}
{"error": 403, "message": "Forbidden"}
{"error": 404, "message": "Resource not found"}
{"error": 405, "message": "Method not allowed"}
{"error": 422, "message": "Unprocessable entity"}
{"error": 500, "message": "Server error"}
```

# Example requests

# GET '/actors'
- Fetches a dictionary of actors
- Request Arguments: None
- Request Body: None

Sample Request:
```
GET http: // 0.0.0.0: 8080 / actors
```

Sample Response:
```
{'actors':
[{'age': 20,
'gender': 'Pre-set gender',
'id': 1,
'name': 'Pre-set name'}],
'status': 200,
'success': True,
'total_actors': 1}
```

# GET '/movies'
- Fetches a dictionary of movies
- Request Arguments: None
- Request Body: None

Sample Request:
```
GET http: // 0.0.0.0: 8080 / movies
```

Sample Response:
```
{'movies':
[{'id': 1,
'release_date': 'Mon, 20 Apr 2020 00:00:00 GMT',
'title': 'Pre-set title'}],
'status': 200,
'success': True,
'total_movies': 1}
```

# POST '/actors'
- Posts a new actor to the DB
- Request Arguments: None
- Request Body: New actor name, New actor age, New actor age

Sample Request:
```
POST http: // 0.0.0.0: 8080 / actors
BODY
{
"name": "Test name",
"gender": "Test gender",
"age": 20
}
```

Sample Response:
```
{'actor':
{'age': 20,
'gender': 'Test gender',
'id': 1,
'name': 'Test name'},
'status': 201,
'success': True,
'total_actors': 2}
```

# POST '/movies'
- Posts a new movie to the DB
- Request Arguments: None
- Request Body: New movie title, New movie release_date

Sample Request:
```
POST http: // 0.0.0.0: 8080 / movies
self.new_movie={
"title": "Test title",
"release_date": "2020.04.19"
}
```

Sample Response:
```
{'movie':
{'id': 1,
'release_date': 'Sun, 19 Apr 2020 00:00:00 GMT',
'title': 'Test title'},
'status': 201,
'success': True,
'total_movies': 2}
```

# DELETE '/actors'
- Deletes an actor from the DB
- Request Arguments: Actors ID
- Request Body: None

Sample Request:
```
DELETE http: // 0.0.0.0: 8080 / actors / 1
```

Sample Response:
```
{'deleted': 1,
'status': 200,
'success': True,
'total_actors': 0}
```

# DELETE '/movies'
- Deletes an movie from the DB
- Request Arguments: Movies ID
- Request Body: None

Sample Request:
```
DELETE http: // 0.0.0.0: 8080 / movies / 1
```

Sample Response:
```
{'deleted': 1,
'status': 200,
'success': True,
'total_movies': 0}
```

# PATCH '/actors'
- Patches an actor
- Request Arguments: Actors ID
- Request Body: New name, new age, new gender

Sample Request:
```
PATCH http: // 0.0.0.0: 8080 / actors / 1
```

Sample Response:
```
{'status': 200,
'success': True,
'total_actors': 1,
'updated':
{'age': 99,
'gender': 'female',
'id': 1,
'name': 'Patched name'}}
```

# PATCH '/movies'
- Patches an movie
- Request Arguments: Movies ID
- Request Body: New title, new release_date

Sample Request:
```
PATCH http: // 0.0.0.0: 8080 / movies / 1
```

Sample Response:
```
{'status': 200,
'success': True,
'total_movies': 1,
'updated':
{'id': 1,
'release_date': 'Thu, 01 Jan 2099 00:00:00 GMT',
'title': 'Patched title'}}
```
