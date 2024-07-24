# manage.py
from flask import Flask
from flask_migrate import Migrate, upgrade
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("db-init")
def db_init():
    """Initialize the database"""
    upgrade()

if __name__ == "__main__":
    app.run()



