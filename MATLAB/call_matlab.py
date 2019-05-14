import matlab.engine

def get_emotion_features():
    eng = matlab.engine.start_matlab()
    eng.AbstractFeature(nargout=0)
    return