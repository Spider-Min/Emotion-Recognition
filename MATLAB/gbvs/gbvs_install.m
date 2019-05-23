% addpath('C:\Users\Admin\PycharmProjects\Emotion_Detection\MATLAB\gbvs\util')
% pathroot = pwd;
pathroot = 'C:\Users\Admin\PycharmProjects\Emotion_Detection\MATLAB\gbvs'
save -mat C:\Users\Admin\PycharmProjects\Emotion_Detection\MATLAB\gbvs\util/mypath.mat pathroot
addpath(genpath( pathroot ), '-begin');
savepath