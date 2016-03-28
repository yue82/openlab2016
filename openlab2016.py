# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename


UPLOAD_FOLDER = '/home/tktr/tmp/flask'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/about')
def show_about():
    print "test"
    return render_template('about.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        print "te"
        f = request.files['imgfile']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file', filename=filename))

if __name__ == '__main__':
    # app.debug = True
    app.run()
