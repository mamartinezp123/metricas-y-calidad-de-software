import os
import random
from datetime import timedelta

from flask import Blueprint, request, jsonify, make_response, Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_wtf import CSRFProtect


def is_not_blank(value):
    if value is None or len(value) == 0:
        return True
    else:
        return False


def is_adult(value):
    if value >= 18:
        return True
    return False


class User:
    def __init__(self, name: str, secret: str, age: int):
        self.name = name
        self.secret = secret
        self.age = age

    def get_name(self):
        return self.name

    def get_secret(self):
        return self.secret

    def get_age(self):
        return self.age

    def login(self, name, secret):
        if self.name == name and self.secret == secret:
            return True

    def print_age(self, age):
        print(age)

    def print_name(self, name):
        print(name)

    def print_secret(self, secret):
        print(secret)


class System:
    def __init__(self):
        self.users = []

    def add_user(self, name: str, secret: str, age: int):
        user = User(name, secret, age)
        self.users.append(user)
        return user

    def login_user(self, name: str, secret: str):
        for user in self.users:
            if user.name == name:
                return user.login(name, secret)
        print("Error: User not found")
        return False

    def hash_to_validate(self):
        return str(random.randint(1000, 9999))

    def show_users(self):
        for user in self.users:
            print(f"User: {user.name}, secret: {user.secret}, is adult: {is_adult(user.age)}")

    def get_users(self):
        return self.users

    def delete_user(self, name):
        for user in self.users:
            if user.name == name:
                self.users.remove(user)
                print(f"User {name} deleted")
                return
        print("Error: User not found")


user_bp = Blueprint('user', __name__)

system = System()


@user_bp.route('/users', methods=['POST'])
def create_user():
    is_not_blank(request.json['name'])
    is_not_blank(request.json['secret'])
    user = system.add_user(request.json['name'], request.json['secret'], request.json['age'])
    return jsonify({"name": user.name, "secret": user.secret, "age": user.age}), 201

@user_bp.route('/users/login', methods=['POST'])
def login_user():
    is_not_blank(request.json['name'])
    is_not_blank(request.json['secret'])
    if system.login_user(request.json['name'], request.json['secret']):
        return make_response(
        {'token': create_access_token(identity=system.hash_to_validate())}), 200
    return make_response({"menssage": "Invalid credentials"}), 401


@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return jsonify(system.get_users()), 200


csrf = CSRFProtect()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
app.config["JWT_SECRET_KEY"] = os.getenv("SIGNING_KEY", "default_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.register_blueprint(user_bp)
jwt = JWTManager(app)
csrf.init_app(app)

if __name__ == "__main__":
    system = System()

    name = input("Type your name: ")
    secret = input("Type your secret: ")
    age = input("Type your age: ")

    system.add_user(name, secret, int(age))
    print("User added")

    name = input("Type your name again: ")
    secret = input("Type your secret again: ")

    if system.login_user(name, secret):
        print("Welcome")
    else:
        print("Error")

    print(f"Token generated: {system.hash_to_validate()}")

    system.show_users()

    name = input("Type your name for delete: ")
    system.delete_user(name)

    app.run(host="0.0.0.0", port=5000)
