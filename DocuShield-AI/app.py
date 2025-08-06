from flask import Flask, render_template, request
from scanners.basic_scanner import scan_document
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    if 'document' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['document']
    if file.filename == '':
        return 'No selected file.', 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    result = scan_document(filepath)
    os.remove(filepath)

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
