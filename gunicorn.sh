cd Blues
gunicorn -b 0.0.0.0:8080 --name BluesApp --workers=3 BluesSite:app
