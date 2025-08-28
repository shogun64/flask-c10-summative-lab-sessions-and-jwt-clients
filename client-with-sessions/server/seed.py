from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, User, JournalEntry
from datetime import date

fake = Faker()

with app.app_context():
    print("Deleting all data...")
    User.query.delete()
    JournalEntry.query.delete()

    print("Creating Users...")
    users = []
    usernames = []

    for i in range(5):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(username=username)
        user.password_hash = user.username + 'password'
        users.append(user)
    
    db.session.add_all(users)

    print("Creating entries...")
    entries = []
    for i in range(25):
        contents = fake.paragraph(nb_sentences=8)
        entry = JournalEntry(date=fake.date(), contents=contents)
        entry.user = rc(users)
        entries.append(entry)

    db.session.add_all(entries)
    
    db.session.commit()
    print("Complete.")