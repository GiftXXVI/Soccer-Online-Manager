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

### Email Output

All email output in this documentation is extracted via a Python SMTP Debugging Server.

```bash
python3 -m smtpd -n -c DebuggingServer localhost:8025
```

### Portal
#### POST `/portal/register`
##### Sample Request and Response
```bash
curl -X POST -H "Content-Type:application/json" -d '{"firstname":"Kwabena","lastname":"Santos","date_of_birth":"1999-12-12","email":"k.santos@yahoo.local","password":";;87^child^BORROW^each^04;;"}' http://127.0.0.1:5000/portal/register
```
Or with an optional role parameter:
```bash
curl -X POST -H "Content-Type:application/json" -d '{"firstname":"Kwabena","lastname":"Santos","date_of_birth":"1999-12-12","email":"gift.chimphonda@gmail.local","password":";;87^child^BORROW^each^04;;","role":1}' http://127.0.0.1:5000/portal/register
```
```json
{
  "created": 50,
  "success": true
}
```
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
##### Sample Request and Response
```bash
curl -X POST -H "Content-Type:application/json" -d '{"code":"45777","email":"k.santos@yahoo.local"}' http://127.0.0.1:5000/portal/confirm/50
```
```json
{
  "activated": 50,
  "success": true
}
```
#### POST `/portal/login`
#### Sample Request and Response
```bash
curl -X POST -H "Content-Type:application/json" -d '{"email":"k.santos@yahoo.local","password":";;87^child^BORROW^each^04;;"}' http://127.0.0.1:5000/portal/login
```
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQxODkwOTY0LCJqdGkiOiIxYTcxMzk5Yy1mNmRlLTRmMTktOGI5NS0wYjY5MDUwNjFlOTYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiay5zYW50b3NAeWFob28ubG9jYWwiLCJuYmYiOjE2NDE4OTA5NjQsImV4cCI6MTY0MTg5NDU2NCwic21fcm9sZSI6MH0.ZilMCC5Z577Wdr3HyFB4nxBzZxb5HFSIzm5f3zm9dVY"
}
```
#### POST `/portal/refresh`
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
##### Sample Request and Response
###### Option 1: Provide Only Email
Step 1

```bash
curl -X PATCH -H "Content-Type:application/json" -H "Authorization:Bearer $TOKEN" -d '{"email":"k.santos@yahoo.local"}' http://127.0.0.1:5000/portal/reset
```
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
