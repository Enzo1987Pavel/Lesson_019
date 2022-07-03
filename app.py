from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    # create_database(app, db)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


# def create_database(app, db):  # Функция создания таблицы для пользователей
#     with app.app_context():
#         db.create_all()
#
#         u1 = User(username="test_name", password="test_password", role="test_role")
#
#         with db.session.begin():
#             db.session.add(u1)


app = create_app(Config())

if __name__ == '__main__':
    app.run()
