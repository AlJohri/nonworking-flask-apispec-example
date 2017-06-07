# Example Flask API Microservice

Uses flask-apispec, flask-classful, flask-sqlalchemy, and flask-migrate.

## Quickstart
```
pip3 install -r requirements.txt
export DATABASE_URL=postgresql://localhost/test_app FLASK_APP=app.py
createdb test_app
flask db init
flask db migrate
flask db upgrade
psql $DATABASE_URL -c "INSERT INTO templates (name, namespace, content) VALUES ('lede', 'washpost.hss.football_game.deciding_play', 'This is a sample template.')"
flask run
```

## Endpoints

- http://localhost:5000/
- http://localhost:5000/templates/
- http://localhost:5000/templates/1
