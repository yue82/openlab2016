# -*- coding: utf-8 -*-

import time
import base64
from flask import Flask
from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/about')
def show_about():
    return render_template('about.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/app', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        imgfile = request.files['imgfile']
        if imgfile and allowed_file(imgfile.filename):
            enc_img = base64.b64encode(imgfile.read())

            return render_template('result.html')

if __name__ == '__main__':
    # app.debug = True
    app.run()
