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

#### GET `/accounts/{account_id}`

##### Sample Request and Response

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

#### GET `/accounts/{account_id}/teams/`

##### Sample Request and Response

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

#### POST `/accounts`

##### Sample Request and Response

```bash
curl -X POST -H "Authorization:Bearer $TOKEN2" -H "Content-Type:application/json" -d '{"country":14,"nickname":"slayer102"}' http://127.0.0.1:5000/accounts
```

```json
{
  "created": 17,
  "success": true
}
```

#### PATCH `/accounts`

##### Sample Request and Response

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

### Teams

#### GET `/teams`

##### Sample Request and Response

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

#### GET `/teams/{team_id}`

##### Sample Request and Response

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

#### GET `/teams/{team_id}/players`

##### Sample Request and Response

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

#### PATCH `/team/{team_id}`

##### Sample Request and Response

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

### Players

#### GET `/players`

##### Sample Request and Response

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

#### GET `/players/{player_id}`

##### Sample Request and Response

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

#### PATCH `/players/{player_id}`

##### Sample Request and Response

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

### Transfers

#### GET `/transfers`

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/transfers
```

```json
{
  "accounts": [
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

#### GET `/transfers/state/{state_id}`

##### Sample Request and Response

```bash
curl -X GET -H "Authorization:Bearer $TOKEN2" http://127.0.0.1:5000/transfers/state/0
```

```json
{
  "accounts": [
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

#### PATCH `/transfers`

##### Sample Request and Response

```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"value":"1750000"}' http://127.0.0.1:5000/transfers/3
```

```json
{
  "modified": 3,
  "success": true
}
```

#### DELETE `/transfers`

##### Sample Request and Response

```bash
curl -X DELETE -H "Authorization:Bearer $TOKEN1" http://127.0.0.1:5000/transfers/3
```

```json
{
  "deleted": 3,
  "success": true
}
```

### Bids

#### GET `/bids`
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

```bash
curl -X POST -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"team":9,"value":"1500000"}' http://127.0.0.curl -X POST -H "Authorization:Bearer $TOKEN1" -H "Content-Type:application/json" -d '{"value":"1500000"}' http://127.0.0.1:5000/transfers/4/bids
```

```json
{
  "created": 6,
  "success": true
}
```

#### PATCH `/transfers/{transfer_id}/bids`

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
```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN2"  http://127.0.0.1:5000/bids/select/8
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
```bash
curl -X PATCH -H "Authorization:Bearer $TOKEN1"  http://127.0.0.1:5000/bids/confirm/8
```
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

