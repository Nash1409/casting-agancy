# Full Stack API Final Project

## Full Stack Casting Agency

The Casting Agency models a a system to simplify and streamline process of creating movies and managing and assigning actors to those movies. 

The application has:

1) Display movies and actors - show movies and actors. 
2) Delete movies and actors .
3) Add movies and and actors.
4) Update movies and and actors by providing its id.

### Motivation
I develop this final project (Casting Agency) in order enhance my skills and knowledge that I have learned through this course (FSND).

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/Casting_Agency` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `casting_agancy` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py;
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` to find the application. 

## Database Setup

python manage.py db upgrade

## Authentication

The API has three diffrent users:

1) Casting Assistant

    email: ca@mm.com
    password: 123456Nn
    
    Role: 

        Casting Assistan

    Permissions:

        get:movies
        get:actors

2) Casting Director

    email: cd@mm.com
    password: 123456Cd

    Role: 

        Casting Director

    Permissions:

        get:movies
        patch:actors
        patch:movies
        post:actors
        get:actors
        delete:actors
3) Executive Producer

    email: ED@mm.com
    password: 123456Ed

    Role: 

        Executive Producer

    Permissions:

        get:movies
        get:actors
        patch:actors
        patch:movies
        post:actors
        post:movies
        delete:actors
        delete:movies


### Endpoints

GET '/movies'
- Get lis of movies including title, release_date, and its id.
- Request Arguments: None
- Returns: list of movies that contain title, release_date, and its id, and success message in case of getting the list of movies. otherwise, return the faild message. 

{
    "movies": [
        {
            "id": 4,
            "release_date": "12-09-2013",
            "title": "green zone"
        },
        {
            "id": 2,
            "release_date": "10-10-2010",
            "title": "joy"
        },
        {
            "id": 3,
            "release_date": "10-10-2010",
            "title": "little stars"
        }
    ],
    "success": true
}

GET '/actors'
- Get lis of actors along with their movies including name, age, gender, movie_id and its id.
- Request Arguments: None
- Returns: list of actors that contain name, age, gender, movie_id, and its id, and success message in case of getting the list of actors. otherwise, return the faild message. 

{
    "actors": [
        {
            "age": 55,
            "gender": "Female",
            "id": 3,
            "movie_id": 2,
            "name": "Jinifer"
        },
        {
            "age": 60,
            "gender": "Fmale",
            "id": 5,
            "movie_id": 1,
            "name": "Angelina"
        },
        {
            "age": 65,
            "gender": "male",
            "id": 6,
            "movie_id": 3,
            "name": "Prad"
        },
        {
            "age": 69,
            "gender": "male",
            "id": 7,
            "movie_id": 3,
            "name": "Tom"
        }
    ],
    "success": true
}

POST '/movies'
- Create new movie which required some filds like title, release_date.  
- Request Arguments: title, release_date
- Returns: inserted movie that contains title, release_date, and its id along with success message in case of inserting movie. otherwise, return the faild message.
{
    "movie": {
        "id": 5,
        "release_date": "10-01-2011",
        "title": "27 dress"
    },
    "success": true
}


POST '/actors'
- Create new actor which required some filds like name, age, gender, movie_id.  
- Request Arguments: name, age, gender, movie_id
- Returns: inserted actor that contains name, age, gender, movie_id, and its id along with success message in case of inserting actor. otherwise, return the faild message.

{
    "actors": {
        "age": 69,
        "gender": "male",
        "id": 8,
        "movie_id": 3,
        "name": "Tom"
    },
    "success": true
}


DELETE '/movies/<int:movie_id>'
- Delete the selected movie by movie_id
- Request Arguments: movie_id
- Returns: deleted id of movie along with success message in case of deleting movie. otherwise, return the faild message. 
{
    "deleted": 1,
    "success": true
}

DELETE '/actors/<int:actor_id>'
- Delete the selected actor by actor_id
- Request Arguments: actor_id
- Returns: deleted id of actor along with success message in case of deleting actor. otherwise, return the faild message. 
{
    "deleted": 2,
    "success": true
}

PATCH '/movies/<int:movie_id>'
- update the selected movie by providing some filds like title, release_date.  
- Request Arguments: title, release_date, movie_id
- Returns: updated movie that contains title, release_date, and its id along with success message in case of updating movie. otherwise, return the faild message.

{
    "movies": [
        "green zone",
        "12-09-2013"
    ],
    "success": true
}

PATCH '/actors/<int:actor_id>'
- update the selected actor by providing some filds like name, age, gender, movie_id. 
- Request Arguments: name, age, gender, movie_id, actor_id.
- Returns: updated actor that contains name, age, gender, movie_id, and its id along with success message in case of updating actor. otherwise, return the faild message.

{
    "actors": [
        "Angelina",
        60,
        "Fmale",
        1
    ],
    "success": true
}


### Test

To run the tests, run

dropdb agancy_test
createdb agancy_test

run python3 test_app.py


## DEPLOYMENT

The app is hosted live on heroku at the URL: 
https://casting-agancy.herokuapp.com