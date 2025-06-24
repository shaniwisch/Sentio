from flask import Flask, request, render_template
from deepface import DeepFace
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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

    # שולחים ל-template רק את שם הקובץ (filename), לא את הנתיב המלא
    return render_template('picture.html', picture_filename=file.filename, information=dominant_emotion)

if __name__ == '__main__':
    app.run(debug=True)
