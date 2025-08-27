from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class User(db.Model):
    pass

class JournalEntry(db.Model):
    pass