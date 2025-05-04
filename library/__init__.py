from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config




db=SQLAlchemy()
# migrate = Migrate()

# 
# def create_app(config_name='default'):
def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate = Migrate(app, db)


    from .Books import books as books_blueprint
    app.register_blueprint(books_blueprint, url_prefix='/books')

    from .members import members as members_blueprint
    app.register_blueprint(members_blueprint, url_prefix='/members')

    from .lending import lending as lending_blueprint
    app.register_blueprint(lending_blueprint, url_prefix='/lending')

    return app