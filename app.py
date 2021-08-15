import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
import imghdr


app = Flask(__name__)
app.config['DIRECTORY_PATH'] = 'uploads'
app.config['SIZE_ALLOWED'] = 1024 * 1024 * 4
app.config['EXTENSIONS_ALLOWED'] = ['.jpg', '.png']


def sanitary_check(stream):
    header = stream.read(512)
    stream.seek(0)
    file_format = imghdr.what(None, header)
    if not file_format:
        return None
    return '.' + (file_format if file_format != 'jpeg' else 'jpg')


def delete_previous_files(files):
    for file in files:
        os.remove(os.path.join(app.config['DIRECTORY_PATH'], file))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def results():
    files = os.listdir(app.config['DIRECTORY_PATH'])
    return render_template('results.html',  files=files)


@app.route('/', methods=['POST'])
def file_upload():
    submitted_file = request.files['file']
    filename = secure_filename(submitted_file.filename)
    if len(filename) > 0:
        file_path = os.path.splitext(filename)[1]
        if file_path not in app.config['EXTENSIONS_ALLOWED'] or \
                file_path != sanitary_check(submitted_file.stream):
            abort(400)
        files = os.listdir(app.config['DIRECTORY_PATH'])
        delete_previous_files(files)
        submitted_file.save(os.path.join(app.config['DIRECTORY_PATH'], filename))
        return redirect(url_for('results'))
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['DIRECTORY_PATH'], filename)


if __name__ == '__main__':
    app.run(debug=True)
