from flask import Blueprint, request, jsonify
from flask import current_app
import jwt
from .models import Users, Progress, Lessons, Levels
from . import db

database_utils = Blueprint('database_utils', __name__)


@database_utils.route('/get_progress', methods=['POST'])
def get_progress():
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        request_data = request.get_json()
        lesson_id = request_data.get('currentLesson')

        if not lesson_id:
            return jsonify({'error': 'Lesson ID is missing'})

        progress = Progress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
        return jsonify({'progress': progress.value, 'gesture': progress.last_gesture})
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})


@database_utils.route('/get_levels', methods=['GET'])
def get_levels():
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        levels = Levels.query.all()
        levels_list = []
        for level in levels:
            level_dict = {
                'id': level.id,
                'name': level.name,
                'description': level.description
            }
            levels_list.append(level_dict)

        return jsonify({'success': True, 'levels': levels_list})
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})


@database_utils.route('/get_lessons/<int:level_id>', methods=['GET'])
def get_lessons(level_id):
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        lessons = Lessons.query.filter_by(level_id=level_id).order_by(Lessons.id).all()
        result = []

        for lesson in lessons:
            result.append({
                'id': lesson.id,
                'name': lesson.name,
                'description': lesson.description,
                'level_id': lesson.level_id
            })

        return jsonify(result)
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})


@database_utils.route('/get_lesson/<int:level_id>/<int:lesson_id>', methods=['GET'])
def get_lesson(level_id, lesson_id):
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        lessons = Lessons.query.filter_by(level_id=level_id, id=lesson_id).order_by(Lessons.id).all()
        result = []
        for lesson in lessons:
            result.append({
                'id': lesson.id,
                'name': lesson.name,
                'description': lesson.description,
                'content': lesson.content,
                'level_id': lesson.level_id
            })
        return jsonify(result)
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})


@database_utils.route('/update_progress', methods=['POST'])
def update_progress():
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        request_data = request.get_json()
        lesson_id = request_data.get('currentLesson')
        value = request_data.get('progressValue')
        last_gesture = request_data.get('lastGesture')

        progress = Progress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()

        progress.value = value
        progress.last_gesture = last_gesture
        db.session.commit()
        return jsonify({'success': True})

    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})

