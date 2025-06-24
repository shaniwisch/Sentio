from flask import Flask, request, render_template, send_from_directory
from deepface import DeepFace
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_picture():
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    save_path = os.path.join('static', 'images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = os.path.join(save_path, file.filename)
    file.save(file_path)

    result = DeepFace.analyze(img_path=file_path, actions=['emotion'], enforce_detection=False)
    dominant_emotion = result[0]['dominant_emotion']

    return render_template('picture.html', picture_path=file_path, information=dominant_emotion)

if __name__ == '__main__':
    app.run(debug=True)
