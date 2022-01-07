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
```bash
flask db upgrade
```