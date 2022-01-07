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

#### PATCH `/positions`
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

#### DELETE `/positions`
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
