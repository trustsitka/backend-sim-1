import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from sim.resources.animals import Animal, AddAnimal, Species, AllAnimals
from sim.resources.users import User, UserRegister, UserLogin
from sim.server.db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///../data/simulation.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_SECRET_KEY'] = "v3ry_s3cr3t_k3y"
# app.secret_key = "v3ry_s3cr3t_k3y"

api = Api(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 401
    )


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader",
            "error_msg": error
        }, 401
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )


api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Animal, "/animal/<int:id>")
api.add_resource(AddAnimal, "/add")
api.add_resource(Species, "/species/<species>")
api.add_resource(AllAnimals, "/animals")

if __name__ == '__main__':
    # import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(port=5000, debug=True)
