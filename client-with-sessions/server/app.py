from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, JournalEntry
from schemas import UserSchema, JournalEntrySchema

class Signup(Resource):
    def post(self):
        pass

class Login(Resource):
    def post(self):
        pass

class Logout(Resource):
    def delete(self):
        pass

class CheckSession(Resource):
    def get(self):
        pass

class Journal(Resource):
    def get(self):
        pass
    def post(self):
        pass

class Entry(Resource):
    def get(self):
        pass
    def patch(self):
        pass
    def delete(self):
        pass

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Journal, '/journal')
api.add_resource(Entry, '/journal/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)