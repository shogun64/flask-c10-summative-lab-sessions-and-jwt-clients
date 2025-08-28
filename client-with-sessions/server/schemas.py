from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    journal_entries = fields.Nested(lambda: JournalEntrySchema(exclude=("user",)),many=True)

class JournalEntrySchema(Schema):
    id = fields.Int()
    date = fields.Date()
    contents = fields.String()
    user = fields.Nested(lambda: UserSchema(exclude=("journal_entries",)))