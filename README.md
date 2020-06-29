# Casting Agency API

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The link of the API can be accessed at: https://casting-agency-mansour.herokuapp.com/


The production app can be accessed at: (https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

## Getting Started

To get started, clone the repo to your local machine by running:

```bash
git clone https://github.com/Mansour-Aldundur/Casting-Agency.git
```

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in th
 [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the 
[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Setting up the app

From within the root directory of the project, first ensure you are working using your created virtual environment.

Make sure you edit the `DATABASE_URL` variable in the `setup.sh` file to reflect the actual database url of your database, then run:

```bash
source setup.sh
```

This will setup the environment variables and run database migrations.

### Running the server

After the setup is complete, run the app using the command below:

```bash
flask run
```

### Accessing the endpoints

A third-party authentication service [Auth0](https://auth0.com) is used to handle authentication needs in the application and Role-Based-Access-Control is implemented in the app, which means authentication headers which contain JWT tokens and the required permissions will be used to access the endpoints.

For convenience, and for review purposes, the JWT tokens in the test_app.py can be used for accessing the endpoints.

```bash
NOTE: Tokens will expire in 24 hours.
```

### Testing

To run tests, first edit the `DATABASE_URL_TEST` variable in the `test_app.sh` file to reflect your test database url, then run:

```bash
source test_app.sh
```

This will setup the test environment variables and run the tests.


## API Reference

```
Endpoints
GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors/<id>'
PATCH '/movies/<id>'
DELETE '/movies/<id>'
DELETE '/movies/<id>'

GET '/actors'
- Fetches the list of actors in the database
- Request Arguments: None
- Response:

{
  "actors": [
    {
      "age": 57,
      "gender": "male",
      "id": 1,
      "name": "Steve carell"
    },
    {
      "age": 51,
      "gender": "male",
      "id": 2,
      "name": "Will Smith"
    },
    {
      "age": 31,
      "gender": "female",
      "id": 3,
      "name": "Ema Watson"
    }
  ],
  "message": "successfully returned all actors",
  "success": true
}

GET '/movies'
- Fetches the list of movies in the database
- Request Arguments: None
- Response:
{
  "message": "successfully returned all movies",
  "movies": [
    {
      "id": 1,
      "release_date": "Wed, 11 Aug 2010 00:00:00 GMT",
      "title": "Saw 3"
    },
    {
      "id": 2,
      "release_date": "Fri, 10 Jul 2009 00:00:00 GMT",
      "title": "Die Hard 2"
    }
  ],
  "success": true
}

POST '/actors'
- Add actors to the database 
- Request Body: {
    "name": "Opera",
    "age": 52,
    "gender": "female",
  }
- Response:
{
  "actor": {
    "age": 52,
    "gender": "female",
    "id": 4,
    "name": "Opera"
  },
  "message": "successfully added actor",
  "success": true
}

POST '/movies'
- Add movies to the database 
- Request Body: {
    "title": "Gold one piece",
    "release_date": "10-9-2016"
  }
- Response:
{
  "message": "successfully added movie",
  "movie": {
    "id": 3,
    "release_date": "Sun, 09 Oct 2016 00:00:00 GMT",
    "title": "Gold one piece"
  },
  "success": true
}

PATCH '/actors/<id>'
- Update an actor in the database
- Request Parameters: id
- Request Body: {
    "age": 31,
  }
- Response:
{
  "actor": {
    "age": 31,
    "gender": "female",
    "id": 4,
    "name": "Opera"
  },
  "message": "successfully updated actor details",
  "success": true
}

PATCH '/movies/<id>'
- Update a movie in the database
- Request Parameters: id
- Request Body: {
    "title": "Gold"
  }
- Response:
{
  "message": "successfully updated movie details",
  "movie": {
    "id": 3,
    "release_date": "Sun, 09 Oct 2016 00:00:00 GMT",
    "title": "Gold"
  },
  "success": true
}

DELETE '/actors/<id>'
- Deletes an actor with the specified id
- Request Parameters: id
- Response:
{
  "deleted_id": 4,
  "message": "successfully deleted actor",
  "success": true
}

DELETE '/movies/<id>'
- Deletes a movie with the specified id
- Request Parameters: id
- Response:
{
  "deleted_id": 3,
  "message": "successfully deleted movie",
  "success": true
}


The server returns these types of errors

400 - Bad Request
  {
    "success": false, 
    "error": 400,
    "message": "bad request"
  }

404 - Resource Not Found
  {
    "success": false, 
    "error": 404,
    "message": "resource not found"
  }

405 - Method not allowed
  {
    "success": false, 
    "error": 405,
    "message": "Method not allowed"
  }

422 - Unprocessable entity
  {
    "success": false, 
    "error": 422,
    "message": "unprocessable
  }

```
