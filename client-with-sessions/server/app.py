from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, JournalEntry
from schemas import UserSchema, JournalEntrySchema

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"errors": "Username and password required"}, 422
        
        user = User(username=username)
        user.password_hash = password
        
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
        except IntegrityError:
            db.session.rollback()
            return {'errors': ["Username must be unique."]}, 422
        except ValueError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422
        return UserSchema().dump(user), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {'error': 'Username and password required.'}, 401
        
        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200
        else:
            return {'error': 'Invalid username or password.'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        else:
            return {"error": "User is already logged out" }, 401

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return UserSchema().dump(user), 200
        else:
            return {"error": "User is not logged in"}, 401

class Journal(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        pagination = JournalEntry.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False)
        entries = pagination.items

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "moods": [JournalEntrySchema().dump(entry) for entry in entries]
        }, 200
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        data = request.get_json()

        date = data.get('date')
        contents = data.get('contents')

        if not date:
            return {'errors': 'Date required'}, 422
        elif not contents or len(contents) < 50:
            return {'errors': 'Journal entry must be 50 characters or more'}, 422
        
        journal_entry = JournalEntry(
            date=date,
            contents=contents,
            user_id=user_id
        )

        try:
            db.session.add(journal_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422

        return JournalEntrySchema().dump(journal_entry), 201

class Entry(Resource):
    def get(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        journal_entry = JournalEntry.query.filter_by(id=id, user_id=user_id).first()
        if not journal_entry:
            return {'error': 'Journal entry not found'}, 404
        return JournalEntrySchema().dump(journal_entry), 200
    def patch(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        journal_entry = JournalEntry.query.filter_by(id=id, user_id=user_id).first()
        if not journal_entry:
            return {'error': 'Journal entry not found'}, 404
        data = request.get_json()
        journal_entry.contents = data['contents']
        db.session.commit()
        return {'message': 'Journal entry updated'}, 200
    def delete(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        journal_entry = JournalEntry.query.filter_by(id=id, user_id=user_id).first()
        if not journal_entry:
            return {'error': 'Journal entry not found'}, 404
        db.session.delete(journal_entry)
        db.session.commit()
        return {'message': 'Journal entry deleted'}, 200

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Journal, '/journal')
api.add_resource(Entry, '/journal/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)