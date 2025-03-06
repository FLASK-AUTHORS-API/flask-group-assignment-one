from flask import Flask
from app.extensions import db, migrate, jwt
from app.controllers.auth.auth_controller import auth

def create_app():
    #application factory function
    app = Flask (__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #importing and registering models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book


    #registering blueprints
    app.register_blueprint(auth)



    @app.route('/')
    def home():
        return 'Authors API Flask Project 1'
    
    return app