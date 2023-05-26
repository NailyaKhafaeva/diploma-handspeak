from . import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    progress = db.relationship('Progress', backref='users', lazy=True)

class Levels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    lessons = db.relationship('Lessons', backref='levels', lazy=True)

class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    progress = db.relationship('Progress', backref='lessons', lazy=True)
    content = db.Column(db.Text, nullable=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    last_gesture = db.Column(db.Integer, nullable=False)

