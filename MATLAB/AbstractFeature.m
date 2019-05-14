addpath('C:\Users\Admin\PycharmProjects\new_flask\MATLAB\Balance\siftDemoV4')
% %traversal all images
% path = 'C:\Users\Admin\PycharmProjects\new_flask\images\';
% fileExt = '*.jpg';  
% files = dir(fullfile(path,fileExt));
% len = size(files,1);  
fid = fopen('C:\Users\Admin\PycharmProjects\new_flask\image_data.txt','w');
% for i=1:len
% fileName = strcat(path,files(i,1).name), 
maindir = 'C:\Users\Admin\Desktop\data';
subdir  = dir( maindir );

for i = 1 : length( subdir )
    if( isequal( subdir( i ).name, '.' )||...
        isequal( subdir( i ).name, '..')||...
        ~subdir( i ).isdir)               % 如果不是目录则跳过
        continue;
    end
    subdirpath = fullfile( maindir, subdir( i ).name, '*.jpg' );
    files = dir( subdirpath )               % 子文件夹下找后缀为dat的文件
    len = size(files,1); 

    for j = 1 : len
        fileName = fullfile( maindir, subdir( i ).name, files( j ).name)
        img = imread(fileName);
        %define the label
        if subdir(i).name == "A"
            fprintf(fid,'6 ');
        elseif subdir(i).name == "Am"
            fprintf(fid,'0 ');
        elseif subdir(i).name == "F"
            fprintf(fid,'2 ');
        elseif subdir(i).name == "D"
            fprintf(fid,'4 ');
        elseif subdir(i).name == "S"
            fprintf(fid,'7 ');
        elseif subdir(i).name == "E"
            fprintf(fid,'3 ');
        end
        %generate balance vector
        out1 = symmetry(img,'mirror',0.8);
        fprintf(fid,'1:%f 2:%f 3:%f 4:%f ',out1);
        out2 = symmetry(img,'rotational');
        fprintf(fid,'5:%f 6:%f ',out2);
        S = FRST(double(img), 5);
        fprintf(fid,'7:%f ',S);
        %generate movement vector
        [gaze_vector] = movement(img);
        fprintf(fid,'8:%f 9:%f 10:%f 11:%f 12:%f 13:%f 14:%f 15:%f 16:%f 17:%f ',gaze_vector);
        %generate emphasis vector
        [RFA] = emphasis(img);
        fprintf(fid,'18:%f ',RFA);
        %generate gradation vector
        [RG,AGTx,AGTy,AGIx,AGIy] = get_Gradation(fileName);
        fprintf(fid,'19:%f 20:%f 21:%f 22:%f 23:%f ',RG,AGTx,AGTy,AGIx,AGIy);
        %generate variety vector
        [variety] = get_Variety(fileName);
        fprintf(fid,'24:%f 25:%f 26:%f 27:%f 28:%f 29:%f 30:%f 31:%f 32:%f 33:%f 34:%f\n',variety);
    end;  
end;
fclose(fid);













