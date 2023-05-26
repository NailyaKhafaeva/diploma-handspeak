import base64
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file
import io
from PIL import Image
import cv2
import numpy as np
from flask import Flask, request, send_file
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from flask import current_app
import jwt


main = Blueprint('main', __name__)


@main.route('/image_handle', methods=['POST'])
def upload_image():
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Authorization token is missing'})

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid token'})

        file = request.files['image']
        gesture = request.form['number']
        level = request.form['level']
        classifier = 0;

        if (int(level) == 1):
            classifier = load_model('numbers.h5')
        else:
            classifier = load_model('letters.h5')

        print(type(classifier))
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        frame_1 = img_to_array(img)

        frame = cv2.flip(frame_1, 1)
        roi = frame[100:400, 320:620]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        copy = frame.copy()
        cv2.rectangle(copy, (320, 100), (620, 400), (255, 0, 0), 5)
        roi = roi.reshape(1, 28, 28, 1)
        roi = roi / 255
        result = classifier.predict(roi)
        number = np.argmax(result)

        if (number == int(gesture)):
            gesture = 1
        else: gesture = 0

        if (int(level) == 1):
            cv2.putText(copy, str(number), (300, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
        else:
            dictionary = {0: 'A', 1: 'B', 2: 'Г', 3: 'Е', 4: 'Ж', 5: 'И', 6: 'Л', 7: 'М', 8: 'Н', 9: 'О', 10: 'П', 11: 'Р',
                          12: 'С', 13: 'Т', 14: 'У', 15: 'Ф', 16: 'Х', 17: 'Ч', 18: 'Ш', 19: 'Ы', 20: 'Э', 21: 'Ю', 22: 'Я'}
            cv2.putText(copy, str(dictionary[number]), (300, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)

        # Convert the OpenCV image to RGB color space
        copy_rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)

        # Create PIL image
        image2 = Image.fromarray(np.uint8(copy_rgb))

        # Create an in-memory file object
        file_object = io.BytesIO()
        image2.save(file_object, 'PNG')
        file_object.seek(0)

        encoded_string = base64.b64encode(file_object.getvalue()).decode('utf-8')

        response = {
            'image': 'data:image/png;base64, ' + encoded_string,
            'result': gesture
        }

        response_json = jsonify(response)
        return response_json
    except jwt.exceptions.DecodeError:
        return jsonify({'error': 'Invalid11 token'})



