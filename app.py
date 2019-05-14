# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory, render_template, redirect
from werkzeug.utils import secure_filename
import image_emotion_gender_demo
from datetime import timedelta



import sys
import time
sys.path.append("C:\\Users\\Admin\\PycharmProjects\\Emotion_Detection\\MATLAB")
from MATLAB.call_matlab import get_emotion_features

from prediction_emotion_paef import predict_emotion_paef

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# html = '''
#     <!DOCTYPE html>
#     <title>Upload File</title>
#     <h1>Photo Upload</h1>
#     <form method=post enctype=multipart/form-data>
#          <input type=file name=file>
#          <input type=submit value=upload>
#     </form>
#     '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    context = {'flag':False}
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = "emotion_image.jpg"
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            context['flag'] = True
            context['file_url'] = file_url
            # context['val1'] = time.time()
            emoji = image_emotion_gender_demo.emotion_identify(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if emoji == False:
                get_emotion_features()

                context['emotion'] = predict_emotion_paef('C:/Users/Admin/PycharmProjects/Emotion_Detection/image_data.txt')
                print(context['emotion'])

            else:
                context['emotion'] = emoji


            # return html + '<br><img src=' + file_url + '>'
            # render_template("index.html", **context)
    return render_template("index.html", **context)
    # return html


if __name__ == '__main__':
    app.run()