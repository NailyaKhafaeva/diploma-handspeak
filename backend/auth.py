from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import jwt
from datetime import datetime, timedelta
from .models import Users, Progress, Lessons
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')

    if not email or not password:
        error = 'Please provide both email and password.'
        return jsonify({'success': False, 'error': error})

    user = Users.query.filter_by(email=email).first()
    if not user:
        error = 'User with this email does not exist.'
        return jsonify({'success': False, 'error': error})

    if not check_password_hash(user.password, password):
        error = 'Invalid password.'
        return jsonify({'success': False, 'error': error})

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'])

    return jsonify({'success': True, 'token': token})


@auth.route('/signup', methods=['POST'])
def signup_post():
    request_data = request.get_json()
    username = request_data.get('username')
    email = request_data.get('email')
    password = request_data.get('password')

    user = Users.query.filter_by(email=email).first()

    if user:
        error = 'User with this email already exists.'
        return jsonify({'success': False, 'error': error})

    user_hash = generate_password_hash(password, method='sha256')
    new_user = Users(name=username, email=email, password=user_hash)

    db.session.add(new_user)
    db.session.commit()

    lessons = Lessons.query.all()
    for lesson in lessons:
        new_progress = Progress(user_id=new_user.id, lesson_id=lesson.id, value=0, last_gesture=0)
        db.session.add(new_progress)
    db.session.commit()

    return jsonify({'success': True})

