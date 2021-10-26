from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from model import *
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

        f0 = request.files['file-0']
        f1 = request.files['file-1']

        if f0.filename.rsplit('.', 1)[1].lower() != 'csv' or f1.filename.rsplit('.', 1)[1].lower() != 'csv':
            response = {'error': 'Only csv files are allowed'}
            return response, 406

        filename0 = secure_filename(f0.filename)
        filename1 = secure_filename(f1.filename)

        filepath0 = os.path.join(app.config['UPLOAD_FOLDER'], filename0)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        f0.save(filepath0)
        f1.save(filepath1)

        d = stockModel(filepath0, filepath1)
        response = {'msg': 'File Uploaded Successfully'}
        return d


if(__name__ == '__main__'):
    app.run(debug=True)
