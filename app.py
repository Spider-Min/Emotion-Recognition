# -*- coding: utf-8 -*-
import os
import random
from flask import Flask, request, url_for, send_from_directory, render_template, redirect
from werkzeug.utils import secure_filename
import image_emotion_gender_demo
from datetime import timedelta
import shutil
import random



import sys
import time
sys.path.append("C:\\Users\\Admin\\PycharmProjects\\Emotion_Detection\\MATLAB")
from MATLAB.call_matlab import get_emotion_features
from os import listdir
from os.path import isfile, join
from prediction_emotion_paef import predict_emotion_paef

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

'''
    utlit 
'''


# # read test pictures
# g = os.walk("./static/test/")
# i = 0
# filepath_list = []
#
# for path, dir_list, file_list in g:
#     for file_name in file_list:
#         filepath = os.path.join(path, file_name)
#
#         if "DS_Store" not in filepath:
#             filepath_list.append(filepath)
#             # print(filepath)
#             # f.write(filepath + "\t" + predict_labels[i].strip() + "\n")
#             # test_picurl.append((filepath, predict_labels[i].strip()))
#             i += 1
#             # print(os.path.join(path, file_name))
#
# filepath_list.sort()
#
# # read test pictures predict label
# with open("predict_result.txt", "r") as predict_f:
#     predict_labels = predict_f.readlines()
#
# with open("test_pictures_url_predictLabel.txt", "w") as f:
#     for i in range(len(filepath_list)):
#         f.write(filepath_list[i] + "\t" + predict_labels[i].strip() + "\n")
# print(sorted(filepath_list))

mapping = {
   0: "happy",
   2: "fear",
   3: "excitement",
   4: "disgust",
   6: "anger",
   7: "sad"
}

pridect_result = {}
test_picurl = []

with open("test_pictures_url_predictLabel.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip().split("\t")
        pridect_result[line[0]] = line[1]
        test_picurl.append(line[0])

# print(pridect_result)

random.shuffle(test_picurl)

cnt = 0
question_num = 10

def genteratePics():
    global cnt
    res = []
    for i in range(question_num):
        res.append(test_picurl[cnt])
        cnt += 1
        if cnt == 179:
            random.shuffle(test_picurl)
            cnt = 0

    return res

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
            demo_dir = "./static/demo_images"+"/" + context['emotion']
            files = [f for f in listdir(demo_dir) if isfile(join(demo_dir, f))]
            random.shuffle(files)
            print(files)
            res_files = ""
            for i in range(5):
                res_files += files[i].split(".")[0]
                if i < 4:
                    res_files += ","
            context['names'] = res_files



    # if request.method == 'GET':
    #         # read test pictures
    #         g = os.walk("./test_images/")
    #         for path, dir_list, file_list in g:
    #             for file_name in file_list:
    #                 filepath = os.path.join(path, file_name)
    #                 new_filename = "emotion_image.jpg"
    #                 shutil.copyfile(filepath, os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    #                 file_url = url_for('uploaded_file', filename=new_filename)
    #                 context['flag'] = True
    #                 context['file_url'] = file_url
    #                 # context['val1'] = time.time()
    #                 emoji = image_emotion_gender_demo.emotion_identify(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    #                 if emoji == False:
    #                     get_emotion_features()
    #                     context['emotion'] = predict_emotion_paef('C:/Users/Admin/PycharmProjects/Emotion_Detection/image_data.txt')
    #                     print(context['emotion'])
    #
    #                 else:
    #                     context['emotion'] = emoji
    #                 with open("C:/Users/Admin/PycharmProjects/Emotion_Detection/system_predict.txt",'a') as wf:
    #                     wf.write(file_name + "\t" + context['emotion'] + "\n")


            # return html + '<br><img src=' + file_url + '>'
            # render_template("index.html", **context)
    return render_template("index.html", **context)
    # return html


currentTestPics = []
@app.route('/evaluation', methods=['GET', 'POST'])
def evaluation():
    global currentTestPics
    context = {}
    if request.method == 'POST':
        evaluation_result = request.json['data']
        print(evaluation_result)
        i = 0
        with open("evaluation_result.txt", "a") as f:
            for pic_path in currentTestPics:
                systemPredict_label = mapping[int(pridect_result[pic_path])]
                groundTrue_label = pic_path.split("/")[-1].split("_")[0]
                user_label = evaluation_result[str(i)]

                if groundTrue_label in user_label:
                    result_abs = "True"
                else:
                    result_abs = "False"

                if systemPredict_label in user_label:
                    result_sys = "True"
                else:
                    result_sys = "False"

                i += 1
                f.write(pic_path + "\t" + groundTrue_label + "\t" + systemPredict_label + "\t" + ",".join(user_label) + "\t" + result_abs + "\t" + result_sys + "\n")

        return "success"
        # file = request.files['file']
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     file_url = url_for('uploaded_file', filename=filename)
        #     return html + '<br><img src=' + file_url + '>'
    else:
        currentTestPics = genteratePics()
        context["picUrl"] = currentTestPics
        return render_template("evaluation.html", **context)

if __name__ == '__main__':
    app.run()