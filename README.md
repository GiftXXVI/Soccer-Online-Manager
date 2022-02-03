# Soccer Manager API

## Introduction

The Soccer Manager API is a web API for trading virtual football players. It is a Flask based API backend designed to be used with a Javascript based frontend client.

The motivation behind its development is to create a simple, secure API for creating players, teams and trading players between teams.

The API code has been written according to [pep8 guidelines](http://www.python.org/dev/peps/pep-0008/).

## Getting Started

Base URL: the API can be accessed at the following URL `http://127.0.0.1:5000`

Authentication: The API requires a valid Token to accompany every request before access can be granted depending on the claims present in the Token and the identity of the user.

## Dependencies

Install all dependencies by running the following command from the root directory (preferably inside a virtual environment):

```bash
pip install -r requirements.txt
```

## Tech Stack/Tools
The project has been developed using the following tech stack:

Python 3.8.10
PostgreSQL 12
The versions of all libraries can be found in the file requirements.txt

The code was written in Visual Studio Code 1.62.0 on Windows 10 WSL inside Ubuntu 20.04.3 LTS.

## Databases

The API depends on the presence of a postgresql database, whose name should be properly configured in the `LIVEDB_NAME` environment variable.

The live database can be created using the following command:

```bash
sudo -u postgres createdb soccer_online_manager
```

Unit Tests should depend on the presence of a postgresql database, whose name should be properly configured in the `TESTDB_NAME` environment variable.

The test database can be created using the following command:

```bash
sudo -u postgres createdb soccer_online_manager_test
```
After both databases (live and test) have been created, update their schema by running migrations against each database (make sure that the FLASK_APP environment variable is defined before running the command).

```bash
flask db upgrade
```

If the database service is not running, it may be necessary to start it using the following command:

```bash
sudo service postgresql start
```

### Installation

To start the web API; make sure that the database service is running, if it is not yet running; start it using the following command:

```bash
sudo service postgresql start
```
then navigate to the root directory and run the following commands:

```bash
export LIVEDB_NAME={database_name}
export LIVEDB_USER={username}
export LIVEDB_PASS={password}
export LIVEDB_HOST={hostname}
export LIVEDB_PORT={port_number}
export TESTDB_NAME={test_database_name}
export TESTDB_USER={test_username}
export TESTDB_PASS={test_password}
export TESTDB_HOST={test_hostname}
export TESTDB_PORT={test_port_number}
export FLASK_APP=api
export FLASK_ENV=development
```
To start the application, run the following command:

```bash
flask run
```

However, it may also be run using gunicorn (a production ready web server) as follows:

```bash
gunicorn --bind 0.0.0.0:5000 api:app
```

## Unit Tests

Unit tests depend on the test environment variables as defined in the [Getting Started](#Getting-Started) section above.
Unit tests can be defined in the `tests` directory and they should be run by running the file `test.py` as follows:

```bash
python3 test.py
```
## API Reference

### Errors

Errors are returned in the following format:

```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```

Every error response contains a the HTTP status code under the index `error`, a boolean result `false` under the index `success` and a brief message describing the error under the index `message`.

In the event of an error, the API may return one of the following HTTP status codes:

- `404`: not found
- `401`: unauthorized
- `403`: forbidden
- `405`: not allowed
- `422`: unprocessable
- `400`: bad request
- `500`: server error

## User Claims

Users can be created with the role_id claim. This is stored as a credential attribute in the database. Setting this value to 1 gives the credential elevated permissions in certain areas of the system (for example; the ability to view all Teams or all Players).


### Resource Endpoint Library

#### Email Output

All email output in this documentation is extracted via a Python SMTP Debugging Server.

```bash
python3 -m smtpd -n -c DebuggingServer localhost:8025
```

#### Portal

##### POST `/portal/register`

###### Description

This endpoint is used to create a user credential.

###### Request Body

The request body should have the details of the user such as their: 
- firstname
- lastname
- date of birth
- email
- password

###### Response Body

The normal response contains the id of the created user and a success value of True.

###### Sample Request and Response

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"firstname":"Kwabena","lastname":"Santos","date_of_birth":"1999-12-12","email":"k.santos@yahoo.local","password":";;87^child^BORROW^each^04;;"}' http://127.0.0.1:5000/portal/register
```

Or with an optional role parameter:

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"firstname":"Koffi","lastname":"Sato","date_of_birth":"1999-12-12","email":"koffi.sato@gmail.local","password":";;87^child^BORROW^each^04;;","role":1}' http://127.0.0.1:5000/portal/register
```

```json
{
  "created": 50,
  "success": true
}
```

It will also generate an email message to the user requesting them to verify their account as shown below.

```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: 7bit'
b'MIME-Version: 1.0'
b'Subject: Please confirm your email address.'
b'From: no-reply@soccermanager.local'
b'To: k.santos@yahoo.local'
b'X-Peer: 127.0.0.1'
b''
b'Your account has been created at 2022-01-11 10:45:42.'
b'                        The request id is 50.'
b'                        You are required confirm your email address.'
b'                        The confirmation code is 45777.'
b'                        '
------------ END MESSAGE ------------
```

#### POST `/portal/confirm/{credential_id}`

###### Description

This endpoint is used to confirm a user credential email address.

###### Request Body

The request body should have the confirmation code and the email address of the user.

###### Response Body

The normal response contains the id of the activated user and a success value of True.

##### Sample Request and Response

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"code":"45777","email":"k.santos@yahoo.local"}' http://127.0.0.1:5000/portal/confirm/50
```

```json
{
  "activated": 50,
  "success": true
}
```

#### POST `/portal/login`

###### Description

This endpoint is used to login using a user credential.

###### Request Body

The request body should have the details of the user such as their: 
- email
- password

###### Response Body

The normal response contains the token issued and a success value of True.

#### Sample Request and Response

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"email":"k.santos@yahoo.local","password":";;87^child^BORROW^each^04;;"}' http://127.0.0.1:5000/portal/login
```

```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQxODkwOTY0LCJqdGkiOiIxYTcxMzk5Yy1mNmRlLTRmMTktOGI5NS0wYjY5MDUwNjFlOTYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiay5zYW50b3NAeWFob28ubG9jYWwiLCJuYmYiOjE2NDE4OTA5NjQsImV4cCI6MTY0MTg5NDU2NCwic21fcm9sZSI6MH0.ZilMCC5Z577Wdr3HyFB4nxBzZxb5HFSIzm5f3zm9dVY"
}
```

#### POST `/portal/refresh`

###### Description

This endpoint is used to refresh a user token before expiry.

###### Request Body

The request body should have the users email address and the current token.

###### Response Body

The normal response contains the new token and a success value of True.

##### Sample Refresh and Response

```bash
export TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQxODkwOTY0LCJqdGkiOiIxYTcxMzk5Yy1mNmRlLTRmMTktOGI5NS0wYjY5MDUwNjFlOTYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiay5zYW50b3NAeWFob28ubG9jYWwiLCJuYmYiOjE2NDE4OTA5NjQsImV4cCI6MTY0MTg5NDU2NCwic21fcm9sZSI6MH0.ZilMCC5Z577Wdr3HyFB4nxBzZxb5HFSIzm5f3zm9dVY
```

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"k.santos@yahoo.local","token":"$TOKEN"}' http://127.0.0.1:5000/portal/refresh
```

```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTg5MTQ4OCwianRpIjoiMDk0YWFjYjctYTE1MC00YzNlLWE4MTAtZGFjZDBiOGUzMDU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imsuc2FudG9zQHlhaG9vLmxvY2FsIiwibmJmIjoxNjQxODkxNDg4LCJleHAiOjE2NDE4OTUwODgsInNtX3JvbGUiOjB9.ORyYHRVm6LGj__IDU1U0XftNyHv7xD48vTkPX7WDeO8"
}
```

#### PATCH `/portal/reset`

###### Description

This endpoint is used to reset a user password.

###### Request Body

The request body should either have the email address, old password and new password (if the user remembers their old password) or only the email address (if they do not remember).

###### Response Body

The normal response contains the id of the user and a success value of True.

##### Sample Request and Response

###### Option 1: Provide Only Email

Step 1

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"k.santos@yahoo.local"}' http://127.0.0.1:5000/portal/reset
```

In this case, a confirmatio code is sent to the email address to be used to set a new password.

```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: 7bit'
b'MIME-Version: 1.0'
b'Subject: You have requested a password reset.'
b'From: no-reply@soccermanager.local'
b'To: k.santos@yahoo.local'
b'X-Peer: 127.0.0.1'
b''
b'You have requested a password reset at 2022-01-11 10:59:22.'
b'                        Please use the code 30937 to set a new password.'
b'                        Otherwise, ignore this email.'
------------ END MESSAGE ------------
```

```json
{
  "reset": 50,
  "success": true
}
```

Step 2

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"k.santos@yahoo.local","password":"C74LptkFL4seJZYQ", "code":"30937"}' http://127.0.0.1:5000/portal/setpassword
```

Once the new password is set, a notification os sent to the users email address again.

```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: quoted-printable'
b'MIME-Version: 1.0'
b'Subject: Your password has been reset.'
b'From: no-reply@soccermanager.local'
b'To: k.santos@yahoo.local'
b'X-Peer: 127.0.0.1'
b''
b'Your password has been reset at 2022-01-11 11:00:39.'
b'                        If you did not initiate this action, please reset you='
b'r password.'
------------ END MESSAGE ------------
```

```json
{
  "reset": 50,
  "success": true
}
```

##### Option 2:Provide email and password

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"k.santos@yahoo.local", "password":"
Evn.ta]9zxP&#Wut", "old_password":"C74LptkFL4seJZYQ"}' http://127.0.0.1:5000/portal/reset
```

In this case, only a single step is required since the user is already authenticated (with a valid token) and knows the account password.


```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: quoted-printable'
b'MIME-Version: 1.0'
b'Subject: Your password has been reset.'
b'From: no-reply@soccermanager.local'
b'To: k.santos@yahoo.local'
b'X-Peer: 127.0.0.1'
b''
b'Your password has been reset at 2022-01-11 11:03:29.'
b'                            If you did not initiate this action, use the code='
b' 12216 to set a new password.'
------------ END MESSAGE ------------
```

```json
{
  "reset": 50,
  "success": true
}
```

### Countries

#### GET `/countries`

###### Description

This endpoint is used to get a list of countries.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of countries and a success value of True.

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/countries
```

```json
{
  "countries": [
    {
      "id": 1,
      "name": "Malawi"
    }
  ],
  "success": true
}
```

#### GET `/countries/{country_id}`

###### Description

This endpoint is used to get a single country.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the country details and a success value of True.

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/countries/54
```

```json
{
  "country": {
    "id": 54,
    "name": "Mozambique"
  },
  "success": true
}
```

#### POST `/countries`

###### Description

This endpoint is used to create a country.

###### Request Body

The request body should have the name of the country.

###### Response Body

The normal response contains the id of the created country and a success value of True.

##### Sample Request and Response

```bash
curl -X POST -H 'Content-Type:application/json' -H "Authorization:Bearer $TOKEN" -d '{"name":"New Zealand"}' http://127.0.0.1:5000/countries
```

```json
{
  "created": 58,
  "success": true
}
```

#### PATCH `/countries/{country_id}`

###### Description

This endpoint is used to modify a country name.

###### Request Body

The request body should have the new name of the country.

###### Response Body

The normal response contains the id of the country and a success value of True.

##### Sample Request and Response

```bash
curl -X PATCH -H 'Content-Type:application/json' -H "Authorization:Bearer $TOKEN" -d '{"name":"Malawi"}' http://127.0.0.1:5000/countries/1
```

```json
{
  "modified": 1,
  "success": true
}
```

#### DELETE `/countries/{country_id}`

###### Description

This endpoint is used to delete a country.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the country and a success value of True.

##### Sample Request and Response

```bash
 curl -X DELETE -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/countries/59
```

```json
{
  "deleted": 59,
  "success": true
}
```

### Cities

#### GET `/cities/{city_id}`

###### Description

This endpoint is used to get a city.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the details of the city and a success value of True.

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/cities/1
```

```json
{
  "city": {
    "country": "Malawi",
    "country_id": 1,
    "id": 1,
    "name": "Lilongwe"
  },
  "success": true
}
```

#### GET `/cities`

###### Description

This endpoint is used to get a list of cities.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of cities a success value of True.

##### Sample Request and Response

```bash
 curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/cities
```

```json
{
  "cities": [
    {
      "country": "Malawi",
      "country_id": 1,
      "id": 1,
      "name": "Lilongwe"
    },
    {
      "country": "Malawi",
      "country_id": 1,
      "id": 3,
      "name": "Blantyre"
    },
    {
      "country": "Ivory Coast",
      "country_id": 26,
      "id": 4,
      "name": "Abidjan"
    },
    {
      "country": "Ghana",
      "country_id": 24,
      "id": 5,
      "name": "Accra"
    },
    {
      "country": "Ethiopia",
      "country_id": 34,
      "id": 6,
      "name": "Addis Ababa"
    }
  ],
  "success": true
}
```

#### POST `/cities`

###### Description

This endpoint is used to create a city.

###### Request Body

The request body should have the name of the city and the country id.

###### Response Body

The normal response contains the id of the city and a success value of True.

##### Sample Request and Response

```bash
 curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"name":"Tete","country_id":54}' http://127.0.
0.1:5000/cities
```

```json
{
  "created": 69,
  "success": true
}
```

#### PATCH `/cities/{city_id}`

###### Description

This endpoint is used to modify a city.

###### Request Body

The request body should have the new name of the city and/or the new country id.

###### Response Body

The normal response contains the id of the city and a success value of True.

##### Sample Request and Response

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"name":"Maputo","country_id":54}' http://127
.0.0.1:5000/cities/39
```

```bash
{
  "modified": 39,
  "success": true
}
```

#### DELETE `/cities/{city_id}`

###### Description

This endpoint is used to delete a city.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the city and a success value of True.

##### Sample Request and Response

```bash
curl -X DELETE -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/cities/70
```

```json
{
  "deleted": 70,
  "success": true
}
```

### Positions

#### GET `/positions`

###### Description

This endpoint is used to get a list of positions.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of positions and a success value of True.

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/positions
```

```json
{
  "positions": [
    {
      "id": 1,
      "initial_players": 3,
      "name": "Goalkeeper"
    },
    {
      "id": 4,
      "initial_players": 6,
      "name": "Defender"
    },
    {
      "id": 5,
      "initial_players": 6,
      "name": "Midfielder"
    },
    {
      "id": 6,
      "initial_players": 5,
      "name": "Attacker"
    }
  ],
  "success": true
}
```

#### GET `/positions/{position_id}`

###### Description

This endpoint is used to get a position.

###### Request Body

The request body should be empty

###### Response Body

The normal response contains the details of the position and a success value of True.

##### Sample Request and Response

```bash
 curl -X GET -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/positions/1
```

```json
{
  "position": {
    "id": 1,
    "initial_players": 3,
    "name": "Goalkeeper"
  },
  "success": true
}
```

#### POST `/positions`

###### Description

This endpoint is used to create a position.

###### Request Body

The request body should have the name of the position and a number of initial players per team in that position.

###### Response Body

The normal response contains the id of the position and a success value of True.

##### Sample Request and Response

```bash
curl -X POST -H 'Content-Type:application/json' -H "Authorization:Bearer $TOKEN" -d '{"name":"GoalKeeper","initial_players":"3"}' http://127.0.0.1:5000/positions
```

```json
{
  "created": 7,
  "success": true
}
```

#### PATCH `/positions/{position_id}`

###### Description

This endpoint is used to modify a position.

###### Request Body

The request body should have the name of the position and the number of initial players in that position per team.

###### Response Body

The normal response contains the id of the position and a success value of True.

##### Sample Request and Response

```bash
curl -X PATCH -H 'Content-Type:application/json' -H "Authorization:Bearer $TOKEN" -d '{"name":"GoalKeeper1","initial_players":"3"}'
 http://127.0.0.1:5000/positions/7
```

```json
{
  "modified": 7,
  "success": true
}
```

#### DELETE `/positions/{position_id}`

###### Description

This endpoint is used to delete.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the position and a success value of True.

##### Sample Request and Response

```bash
curl -X DELETE -H "Authorization:Bearer $TOKEN" http://127.0.0.1:5000/positions/7
```

```json
{
  "deleted": 7,
  "success": true
}
```

### Accounts

#### GET `/accounts`

###### Description

This endpoint is used to get user accounts.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of accounts and a success value of True.

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/accounts
```

```json
{
  "accounts": [
    {
      "email": "gift.chimphonda@gmail.local",
      "id": 17
    },
    {
      "email": "k.santos@yahoo.local",
      "id": 18
    }
  ],
  "success": true
}
```

#### GET `/accounts/me`

###### Description

This endpoint is used to get the logged in users account.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the account details and a success value of True.

```bash
curl -X GET -H "Authorization:Bearer $CREATOR" http://127.0.0.1:5000/accounts/me
```

###### Sample Request and Response

```json
{
  "account": {
    "email": "peter.watanabe@yahoo.local",
    "id": 19
  },
  "success": true
}
```

##### GET `/accounts/{account_id}`

###### Description

This endpoint is used to get an account.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the details of the account and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/accounts/18
```

```json
{
  "account": {
    "email": "k.santos@yahoo.local",
    "id": 18
  },
  "success": true
}
```

##### GET `/accounts/{account_id}/teams/`

###### Description

This endpoint is used to get teams (the system currently restricts a user to a single team) for the account.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the list of teams and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/accounts/18/teams
```

```json
{
  "success": true,
  "teams": {
    "account": "the_urge22",
    "account_id": 18,
    "budget": "5000000",
    "country": "Algeria",
    "country_id": 22,
    "id": 9,
    "value": "20000000"
  }
}
```

##### POST `/accounts`

###### Description

This endpoint is used to create an account, team and players.

###### Request Body

The request body should have the country id of their team and the nickname of the user.

###### Response Body

The normal response contains the id of the created account and a success value of True.

###### Sample Request and Response

```bash
curl -X POST -H "Authorization:Bearer $TOKEN2" -H "Content-Type:application/json" -d '{"country":14,"nickname":"slayer102"}' http://127.0.0.1:5000/accounts
```

```json
{
  "created": 17,
  "success": true
}
```

##### PATCH `/accounts`

###### Description

This endpoint is used to modify the nickname of the user account.

###### Request Body

The request body should have the new nickname.

###### Response Body

The normal response contains the id of the user account and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"nickname":"the_urge22"}' http://127.0.0.1:
5000/accounts/18
```

```json
{
  "modified": 18,
  "success": true
}
```

#### Teams

##### GET `/teams`

###### Description

This endpoint is used to get teams.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of teams and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/teams
```

```json
{
  "success": true,
  "teams": [
    {
      "account": "slayer102",
      "account_id": 17,
      "budget": "5000000",
      "country": "Switzerland",
      "country_id": 14,
      "id": 8,
      "name": "Fkmcduvaeh Vikings",
      "value": "20000000"
    },
    {
      "account": "the_urge22",
      "account_id": 18,
      "budget": "5000000",
      "country": "Algeria",
      "country_id": 22,
      "id": 9,
      "name": "Algiers Shockers 9442",
      "value": "20000000"
    }
  ]
}
```

##### GET `/teams/{team_id}`

###### Description

This endpoint is used to get a team.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains details of the team and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/teams/8
```

```json
{
  "success": true,
  "team": {
    "account": "slayer102",
    "account_id": 17,
    "budget": "5000000",
    "country": "Switzerland",
    "country_id": 14,
    "id": 8,
    "name": "Fkmcduvaeh Vikings",
    "value": "20000000"
  }
}
```

##### GET `/teams/{team_id}/players`

###### Description

This endpoint is used to get players by team id.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the list of players and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/teams/9/players
```

```json
{
  "players": [
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Thu, 11 Jan 2001 00:00:00 GMT",
      "firstname": "Jean-Paul",
      "id": 121,
      "lastname": "Kachingwe",
      "position_id": 1,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Thu, 11 Jan 2001 00:00:00 GMT",
      "firstname": "Kojo",
      "id": 122,
      "lastname": "Watanabe",
      "position_id": 1,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 2003 00:00:00 GMT",
      "firstname": "George",
      "id": 123,
      "lastname": "Fernandez",
      "position_id": 1,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 1997 00:00:00 GMT",
      "firstname": "Yamikani",
      "id": 124,
      "lastname": "Nunez",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Wed, 11 Jan 2006 00:00:00 GMT",
      "firstname": "Alexander",
      "id": 125,
      "lastname": "Leroy",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 2003 00:00:00 GMT",
      "firstname": "William",
      "id": 126,
      "lastname": "SakalaKapalamula",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Mon, 11 Jan 1999 00:00:00 GMT",
      "firstname": "Thomas",
      "id": 127,
      "lastname": "Tanaka",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 1997 00:00:00 GMT",
      "firstname": "Abdalla",
      "id": 128,
      "lastname": "Mendez",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Tue, 11 Jan 1994 00:00:00 GMT",
      "firstname": "Akwesi",
      "id": 129,
      "lastname": "Suleiman",
      "position_id": 4,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Fri, 11 Jan 2002 00:00:00 GMT",
      "firstname": "Adetokunbo",
      "id": 130,
      "lastname": "Svoboda",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Thu, 11 Jan 2001 00:00:00 GMT",
      "firstname": "Mphatso",
      "id": 131,
      "lastname": "Fischer",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Thu, 11 Jan 1996 00:00:00 GMT",
      "firstname": "Charles",
      "id": 132,
      "lastname": "Mofokeng",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Tue, 11 Jan 1994 00:00:00 GMT",
      "firstname": "Yamikani",
      "id": 133,
      "lastname": "Herrera",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 2003 00:00:00 GMT",
      "firstname": "George",
      "id": 134,
      "lastname": "Mendez",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Wed, 11 Jan 2006 00:00:00 GMT",
      "firstname": "Kwabena",
      "id": 135,
      "lastname": "Kumwenda",
      "position_id": 5,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sat, 11 Jan 1997 00:00:00 GMT",
      "firstname": "Jacques",
      "id": 136,
      "lastname": "Suleiman",
      "position_id": 6,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Wed, 11 Jan 2006 00:00:00 GMT",
      "firstname": "Kgomotso",
      "id": 137,
      "lastname": "Sene",
      "position_id": 6,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Wed, 11 Jan 1995 00:00:00 GMT",
      "firstname": "Mphatso",
      "id": 138,
      "lastname": "Martin",
      "position_id": 6,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sun, 11 Jan 1998 00:00:00 GMT",
      "firstname": "Yamikani",
      "id": 139,
      "lastname": "Mwenda",
      "position_id": 6,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Algeria",
      "country_id": 22,
      "date_of_birth": "Sun, 11 Jan 2004 00:00:00 GMT",
      "firstname": "Frederic",
      "id": 140,
      "lastname": "Oliveira",
      "position_id": 6,
      "team": "Algiers Shockers 9442",
      "team_id": 9,
      "transfer_listed": false,
      "value": "1000000"
    }
  ],
  "success": true
}
```

##### PATCH `/team/{team_id}`

###### Description

This endpoint is used to modify a team name.

###### Request Body

The request body should have the new name of the team.

###### Response Body

The normal response contains the id of the team a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN2" -d '{"name":"Lucerne Vikings"}' http://127.0.0.1
:5000/teams/8
```

```json
{
  "modified": 8,
  "success": true
}
```

#### Players



##### GET `/players`

###### Description

This endpoint is used to get players.

###### Request Body

The request body should be empty

###### Response Body

The normal response contains the list of players and a success value of True.

###### Sample Request and Response

```bash
 curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/players
```

```json
{
  "players": [
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Sat, 11 Jan 2003 00:00:00 GMT",
      "firstname": "Kumbukani",
      "id": 101,
      "lastname": "Goncalves",
      "position_id": 1,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Sun, 11 Jan 2004 00:00:00 GMT",
      "firstname": "George",
      "id": 102,
      "lastname": "Petit",
      "position_id": 1,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Sun, 11 Jan 1998 00:00:00 GMT",
      "firstname": "Pierre",
      "id": 103,
      "lastname": "Simon",
      "position_id": 1,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Tue, 11 Jan 1994 00:00:00 GMT",
      "firstname": "Adetokunbo",
      "id": 104,
      "lastname": "Ingabire",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Wed, 11 Jan 2006 00:00:00 GMT",
      "firstname": "Fatsani",
      "id": 105,
      "lastname": "Keita",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Thu, 11 Jan 1996 00:00:00 GMT",
      "firstname": "Abdalla",
      "id": 106,
      "lastname": "Kachingwe",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Sun, 11 Jan 2004 00:00:00 GMT",
      "firstname": "Limbikani",
      "id": 107,
      "lastname": "Barbosa",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Tue, 11 Jan 2005 00:00:00 GMT",
      "firstname": "Jean-Luc",
      "id": 108,
      "lastname": "Leroy",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    },
    {
      "country": "Switzerland",
      "country_id": 14,
      "date_of_birth": "Wed, 11 Jan 1995 00:00:00 GMT",
      "firstname": "Adetokunbo",
      "id": 109,
      "lastname": "Dupont",
      "position_id": 4,
      "team": "Lucerne Vikings",
      "team_id": 8,
      "transfer_listed": false,
      "value": "1000000"
    }
  ],
  "success": true
}
```

##### GET `/players/{player_id}`

###### Description

This endpoint is used to get a player.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the details of the player and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/players/140
```

```json
{
  "player": {
    "country": "Algeria",
    "country_id": 22,
    "date_of_birth": "Sun, 11 Jan 2004 00:00:00 GMT",
    "firstname": "Frederic",
    "id": 140,
    "lastname": "Oliveira",
    "position_id": 6,
    "team": "Algiers Shockers 9442",
    "team_id": 9,
    "transfer_listed": false,
    "value": "1000000"
  },
  "success": true
}
```

##### PATCH `/players/{player_id}`

###### Description

This endpoint is used to modify a player name.

###### Request Body

The request body should have the new firstname and lastname of the player.

###### Response Body

The normal response contains the id of the player and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"firstname":"Rudolfo","lastname":"Oliveira"
}' http://127.0.0.1:5000/players/140
```

```json
{
  "modified": 140,
  "success": true
}
```

#### Transfers

##### GET `/transfers`

###### Description

This endpoint is used to get transfers. Only a user with priviledged access can view all transfers.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the list of transfers and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/transfers
```

```json
{
  "transfers": [
    {
      "date_completed": null,
      "date_listed": "Wed, 12 Jan 2022 07:40:34 GMT",
      "from_team_id": 9,
      "id": 3,
      "player": "Rudolfo Oliveira",
      "player_id": 140,
      "to_team_id": null,
      "transfer_value": "1500000",
      "value_increase": null
    }
  ],
  "success": true
}
```

##### GET `/transfers/state/{state_id}`

###### Description

This endpoint is used to get transfers by state (complete or incomplete). Any user can get transfers by state.

###### Request Body

The request body should be empty

###### Response Body

The normal response contains a list of transfers and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/transfers/state/0
```

```json
{
  "transfers": [
    {
      "date_completed": null,
      "date_listed": "Wed, 12 Jan 2022 07:40:34 GMT",
      "from_team_id": 9,
      "id": 3,
      "player": "Rudolfo Oliveira",
      "player_id": 140,
      "to_team_id": null,
      "transfer_value": "1500000",
      "value_increase": null
    }
  ],
  "success": true
}
```

#### POST `/transfers`

###### Description

This endpoint is used to create a transfer.

###### Request Body

The request body should have the player id, origin team, and transfer value.

###### Response Body

The normal response contains the id of the transfer and a success value of True.

##### Sample Request and Response

```bash
curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN1" -d '{"player_id":"140","from_team_id":"9","transfer_value":1500000}' http://127.0.0.1:5000/transfers
```

```json
{
  "created": 3,
  "success": true
}
```

##### PATCH `/transfers`

###### Description

This endpoint is used to modify a transfer value.

###### Request Body

The request body should have the new value of the transfer.

###### Response Body

The normal response contains the id of the transfer and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"value":"1750000"}' http://127.0.0.1:5000/transfers/3
```

```json
{
  "modified": 3,
  "success": true
}
```

##### DELETE `/transfers`

###### Description

This endpoint is used to delete a transfer.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the transfer and a success value of True.

###### Sample Request and Response

```bash
curl -X DELETE -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/transfers/3
```

```json
{
  "deleted": 3,
  "success": true
}
```

#### Bids

##### GET `/bids`

###### Description

This endpoint is used to get bids.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of bids and a success value of True.

###### Sample Request and Response

```json
curl -X GET -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/bids
```

```bash
{
  "bids:": [
    {
      "bid_value": "1500000",
      "date_of_bid": "Wed, 12 Jan 2022 00:00:00 GMT",
      "id": 8,
      "team_id": 9,
      "transfer_id": 4
    }
  ],
  "success": true
}
```

#### GET `/transfers/{transfer_id}/bids'

###### Description

This endpoint is used to get bids for a transfer.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains a list of bids and a success value of True.

###### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/transfers/4/bids
```

```json
{
  "bids": [
    {
      "bid_value": "1500000",
      "date_of_bid": "Wed, 12 Jan 2022 00:00:00 GMT",
      "id": 8,
      "team_id": 9,
      "transfer_id": 4
    }
  ],
  "success": true
}
```

#### POST `/transfers/{transfer_id}/bids`

###### Description

This endpoint is used to submit a bid.

###### Request Body

The request body should have the value of the bid.

###### Response Body

The normal response contains the id of the bid and a success value of True.

###### Sample Request and Response

```bash
curl -X POST -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"value":"1500000"}' http://127.0.0.1:5000/transfers/4/bids
```

```json
{
  "created": 6,
  "success": true
}
```

#### PATCH `/transfers/{transfer_id}/bids`

###### Description

This endpoint is used to modify the value of a bid.

###### Request Body

The request body should have the new value. 

###### Response Body

The normal response contains the id of the bid and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"value":"1650000"}' http://127.0.0.1:5000/t
ransfers/4/bids
```

```json
{
  "modified": 6,
  "success": true
}
```

#### DELETE `/bids/{bid_id}

###### Description

This endpoint is used to delete a bid.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the bid and a success value of True.

###### Sample Request and Response

```bash
curl -X DELETE -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/bids/7
```

```json
{
  "deleted": 7,
  "success": true
}
```

#### PATCH `/bids/select/{bid_id}`

###### Description

This endpoint is used to select a winning bid.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the bid and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN2"  http://127.0.0.1:5000/bids/select/8
```

An email is also sent to the bidder.

```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: 7bit'
b'MIME-Version: 1.0'
b'Subject: Please confirm your email address.'
b'From: no-reply@soccermanager.local'
b'To: k.santos@yahoo.local'
b'X-Peer: 127.0.0.1'
b''
b'Your bid for the player Kofi Phirihas been selected at 2022-01-12 23:31:54. '
b'Please confirm the transfer to complete the transaction.'
------------ END MESSAGE ------------

```

```json
{
  "modified": 4,
  "success": true
}
```

#### PATCH `/bids/confirm/{bid_id}`

###### Description

This endpoint is used to confirm a transfer.

###### Request Body

The request body should be empty.

###### Response Body

The normal response contains the id of the winning bid and a success value of True.

###### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1"  http://127.0.0.1:5000/bids/confirm/8
```

An email is sent to the creator of the transfer (origin team).

```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: quoted-printable'
b'MIME-Version: 1.0'
b'Subject: Please confirm your email address.'
b'From: no-reply@soccermanager.local'
b'To: gift.chimphonda@gmail.local'
b'X-Peer: 127.0.0.1'
b''
b'The transfer of the player Kofi Phirihas been confirmed at 2022-01-12 23:52:4='
b'3.'
------------ END MESSAGE ------------
```

```json
{
  "modified": 8,
  "success": true
}
```
