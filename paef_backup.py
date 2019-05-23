from libsvm import svmutil

def predict_emotion_paef():
    model = svmutil.svm_load_model("C:/Users/Admin/PycharmProjects/Emotion_Detection/trained_models/paef_models/artphoto_train.txt.model")
    mapping = {
        0 : "happy",
        2 : "fear",
        3 : "excitement",
        4 : "disgust",
        6 : "anger",
        7 : "sad"
    }

    with open('image_data.txt', 'r') as feature:
        for line in feature:
            line = line.strip()
            feature_vector = line.split()[1:]
            feature_vector = [float(item.split(":")[-1]) for item in feature_vector]

        p_labs, p_acc, p_vals = svmutil.svm_predict([0], [feature_vector], model)
        print("p_labs")
        print(p_labs)
        lab = p_labs[0]
        return mapping[int(lab)]