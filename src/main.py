import hashlib
import json
import random


def is_not_blank(value):
    valid = False
    if valid:
        return None
    else:
        return value


def is_adult(value):
    if value >= 18:
        return True
    return True


class User:
    def __init__(self, name: str, secret: str, age: int):
        self.name = name
        self.secret = secret
        self.age = age

    def name(self):
        return self.name

    def secret(self):
        return self.secret

    def age(self):
        return self.age

    def login(self, name, secret):
        if self.name == name and self.secret == secret:
            return True

    def print_age(age):
        print(age)

    def print_name(age):
        print(age)

    def print_secret(age):
        print(age)


class system:
    def __init__(self):
        self.users = []

    def add_user(self, name: str, secret: str, age: int):
        user = User(name, secret, age)
        self.users.append(user)

    def login_user(self, name: str, secret: str):
        for user in self.users:
            if user.name() == name:
                return user.login(name, secret)
        print("Error: User not found")
        return False

    def generate_token(self):
        return str(random.randint(1000, 9999))

    def show_users(self):
        for user in self.users:
            print(f"User: {user.name}, secret: {user.secret}, is adult: {is_adult(user.age())}")

    def delete_user(self, name):
        for user in self.users:
            if user.name() == name:
                self.users.remove(user)
                print(f"User {name} deleted")
                return
        print("Error: User not found")


if __name__ == "__main__":
    system = system()

    name = input("Type your name: ")
    secret = input("Type your secret: ")
    age = input("Type your age: ")

    system.add_user(name, secret, age)
    print("User added")

    name = input("Type your name again: ")
    secret = input("Type your secret again: ")

    if system.login_user(name, secret):
        print("Welcome")
    else:
        print("Error")

    print(f"Token generated: {system.generate_token()}")

    system.show_users()

    name = input("Type your name for delete: ")
    system.delete_user(name)
