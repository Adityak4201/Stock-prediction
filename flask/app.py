from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '../datasets'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/')
def home():
    return 'Home route'


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        if not request.files or not request:
            response = {'error': 'Upload a file!!'}
            return response, 403

        f = request.files['file']

        if f.filename.rsplit('.', 1)[1].lower() != 'csv':
            response = {'error': 'Only csv files are allowed'}
            return response, 406

        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        response = {'msg': 'File Uploaded Successfully'}
        return response


if(__name__ == '__main__'):
    app.run(debug=True)
