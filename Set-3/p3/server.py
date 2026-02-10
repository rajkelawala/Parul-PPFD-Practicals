import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB

@app.route('/')
def home():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('home'))
    
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename,                 as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)