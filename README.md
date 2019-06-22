# pollution-monitor

A flask based web application to manage pollution data recorded by the pollution monitoring system.

This project is being made under Design Practicum IIT Mandi.

Deployed to [Heroku](https://www.heroku.com/) at https://pollution-monitor-flask.herokuapp.com.

## Local Deployment

1. Fork the repository.

2. Clone the forked repository.

```console
git clone https://github.com/user-name/pollution-monitor.git
```

3. Enter the repository.

```console
cd pollution-monitor
```

4. Create a python virtual environment with ```python=python3```.

5. Activate the virtual environment.

6. Install required python packages from requirements.txt.

```console
pip install -r requirements.txt
```

7. Download and install [PostgreSQL](https://www.postgresql.org/download/).

8. Create database ```pollution_db``` in psql. Refer [here](https://www.postgresql.org/docs/9.0/sql-createdatabase.html). 

9. Set environment variables.

```console
export APP_SETTINGS="config.DevelopmentConfig"
```
```console
export DATABASE_URL="postgresql://localhost/pollution_db"
```

10. Remove folder ```migrations``` and migrate database.

```console
rm -rf migrations
```

```console
python manage.py db init
```
```console
python manage.py db migrate
```
```console
python manage.py db upgrade
```

11. Deploy app.

```console
python manage.py runserver
```

12. Visit URL http://127.0.0.1:5000/
