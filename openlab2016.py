# -*- coding: utf-8 -*-

import requests
import base64
import json
from flask import Flask
from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_WIDTH = 600
END_POINT = 'http://www.ai.cs.kobe-u.ac.jp/vision'

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


def call_classification_api(img_base):
    req = {'img': img_base }
    res = requests.post(END_POINT, json=req)
    return res.json()['result']


def create_result_setting(res):
    img_list = []
    for rate, name in res:
        width = int(BASE_WIDTH * float(rate.strip()[:-1]) * 0.01)
        # src = 'static/class/{}.jpg'.format(name.split(' ')[0].split(',')[0]) # for dog data
        src = u'static/class/{}.jpg'.format(name) # for kadono data
        img_list.append({'src': src,
                        'width': width,
                        'name': name,
                        'rate': rate})
    return img_list


@app.route('/app', methods=['GET', 'POST'])
def upload_file(res=None):
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        img_file = request.files['imgfile']
        if img_file and allowed_file(img_file.filename):
            img_base = base64.b64encode(img_file.read())
            res = call_classification_api(img_base)
            img_list = create_result_setting(res)
            return render_template('result.html', img_list=img_list, originimg=img_base)

if __name__ == '__main__':
    # app.debug = True
    app.run()
