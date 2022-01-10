## Getting Started

Created the live database using the following command:

```bash
sudo -u postgres createdb soccer_online_manager
```

and the test database using the following command:

```bash
sudo -u postgres createdb soccer_online_manager_test
```

If the database service is not running, it may be necessary to start it using the following command:

```bash
sudo service postgresql start
```

It may be neccesarry to run migrations using the following command:
In case changes are made to the data model in `model/__init__.py`, it may be necessary to run the 2 comands below to apply the changes to the database tables.

```bash
flask db migrate -m "Changed User Refs to Account"
```

```bash
flask db upgrade
```

## Resource Endpoint Library

### Portal
#### POST `/portal/register`
##### Sample Request and Response
```bash
curl -X POST -H "Content-Type:application/json" -d '{"firstname":"Gift","lastname":"Chimphonda","date_of_birth":"2001-11-13","password":"112hfhj@sjjPPPP","email":"gift@gmail.local"}' http://127.0.0.1:5000/portal/register
```
```json
{
  "created": 6,
  "success": true
}
```
```bash
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: 7bit'
b'MIME-Version: 1.0'
b'Subject: Confirm your account.'
b'From: no-reply@soccermanager.local'
b'To: gift@gmail.local'
b'X-Peer: 127.0.0.1'
b''
b'Please confirm your account. Your code is 73246.'
b' The request id is 6.'
------------ END MESSAGE ------------
```
#### POST `/portal/confirm/{credential_id}`
##### Sample Request and Response
```bash
 curl -X POST -H "Content-Type:application/json" -d '{"code":"73246","email":"gift@gmail.local"}' http://127.0.0.1:5000/portal/confirm/6
```
```json
{
  "activated": 6,
  "success": true
}
```
#### POST `/portal/login`
#### Sample Request and Response
```bash
curl -X POST -H "Content-Type:application/json" -d '{"email":"gift@gmail.local","password":"112hfhj@sjjPPPP"}' http://127.0.0.1:5000/portal/login
```
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQxNzgyNTQ2LCJqdGkiOiI4MGI3ZjFiYi0xM2Y0LTRhMjEtYTZlNy05YzMzMDA5NGNjMTkiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiZ2lmdEBnbWFpbC5sb2NhbCIsIm5iZiI6MTY0MTc4MjU0NiwiZXhwIjoxNjQxNzg2MTQ2fQ.dJDs8aFx41JGvbNvfqI04-h8rw3fwcQuQaPVGrj6u4Q"
}
```
#### POST `/portal/refresh`
##### Sample Refresh and Response
```bash
export TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQxNzgyNTQ2LCJqdGkiOiI4MGI3ZjFiYi0xM2Y0LTRhMjEtYTZlNy05YzMzMDA5NGNjMTkiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiZ2lmdEBnbWFpbC5sb2NhbCIsIm5iZiI6MTY0MTc4MjU0NiwiZXhwIjoxNjQxNzg2MTQ2fQ.dJDs8aFx41JGvbNvfqI04-h8rw3fwcQuQaPVGrj6u4Q
```
```bash
 curl -X POST -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"gift@gmail.local","token":"$TOKEN"}' http://127.0.0.1:5000/portal/refresh
```
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTc4Mjk0MywianRpIjoiMzJkZmQyOGUtMTNmOC00MTljLWI4ZGYtYWFjODk0NTM4YTMyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImdpZnRAZ21haWwubG9jYWwiLCJuYmYiOjE2NDE3ODI5NDMsImV4cCI6MTY0MTc4NjU0M30.9HX_ZBbMQJ4TRmHnFd6Yau7q_l3WoUqbdhjC_VBFbkM"
}
```
### Countries

#### GET `/countries`

##### Sample Request and Response

```bash
curl http://127.0.0.1:5000/countries
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

##### Sample Request and Response

```bash
curl http://127.0.0.1:5000/countries/1
```

```json
{
  "country": {
    "id": 1,
    "name": "Malawi"
  },
  "success": true
}
```

#### POST `/countries`

##### Sample Request and Response

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"Malawi"}' http://127.0.0.1:5000/countries
```

```json
{
  "created": 1,
  "success": true
}
```

#### PATCH `/countries/{country_id}`

##### Sample Request and Response

```bash
curl -X PATCH -H 'Content-Type:application/json' -d '{"name":"Kingdom of Eswatini"}' http://127.0.0.1:5000/countries/3
```

```json
{
  "modified": 3,
  "success": true
}
```

#### DELETE `/countries/{country_id}`

##### Sample Request and Response

```bash
curl -X DELETE http://127.0.0.1:5000/countries/2
```

```json
{
  "deleted": 2,
  "success": true
}
```

### Cities

#### GET `/cities/{city_id}`

##### Sample Request and Response

```bash
curl -X GET http://127.0.0.1:5000/cities/1
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

##### Sample Request and Response

```bash
curl -X GET http://127.0.0.1:5000/cities
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

##### Sample Request and Response

```bash
 curl -X POST -H "Content-Type:application/json" -d '{"name":"Lilongwe","country_id":1}' http://127.0.0.1:5000/cities
```

```json
{
  "created": 1,
  "success": true
}
```

#### PATCH `/cities/{city_id}`

#### Sample Request and Response

```bash
curl -X PATCH -H "Content-Type:application/json" -d '{"name":"Manchester","country_id":4}' http://127.0.0.1:5000/cities/67
```

```bash
{
  "modified": 67,
  "success": true
}
```

#### DELETE `/cities/{city_id}`

#### Sample Request and Response

```bash
 curl -X DELETE http://127.0.0.1:5000/cities/68
```

```json
{
  "deleted": 68,
  "success": true
}
```

### Positions

#### GET `/positions`

##### Sample Request and Response

```bash
curl -X GET http://127.0.0.1:5000/positions
```

```json
{
  "positions": [
    {
      "id": 1,
      "initial_players": 3,
      "name": "Goalkeeper"
    }
  ],
  "success": true
}
```

#### GET `/positions/{position_id}`

##### Sample Request and Response

```bash
curl -X GET http://127.0.0.1:5000/positions/1
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

##### Sample Request and Response

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"GoalKeeper","initial_players":"3"}' http://127.0.0.1:5000/positions
```

```json
{
  "created": 1,
  "success": true
}
```

#### PATCH `/positions/{position_id}`

##### Sample Request and Response

```bash
curl -X PATCH -H 'Content-Type:application/json' -d '{"name":"Goalkeeper","initial_players":"3"}' http://127.0.0.1:5000/positions/1
```

```json
{
  "modified": 1,
  "success": true
}
```

#### DELETE `/positions/{position_id}`

##### Sample Request and Response

```bash
curl -X DELETE http://127.0.0.1:5000/positions/2
```

```json
{
  "deleted": 2,
  "success": true
}
```
