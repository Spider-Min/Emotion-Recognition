function get_symmetry()
img = 'sad_0463.jpg';
file = fopen('result0.txt','w');

out1 = symmetry(img,'mirror',0.8);
disp(out1)
fprintf(file,'%f ',out1);
out2 = symmetry(img,'rotational');
disp(out2)
fprintf(file,'%f ',out2);
out3 = FRST(double(imread(img)), 5);
fprintf(file,'%f ',out3);
end