function [c_RFA, d_RFA, bd_RFA] = emphasis(img)
circle = imread('circle.jpg');
diagonal = imread('diagonal.png');
back_diagonal = imread('backDiagonal.png');

saliency_gbvs = gbvs(img);

[m n t] = size(img);
circle_mask = imresize(circle, [m n]);
diagonal_mask = imresize(diagonal, [m,n]);
back_diagonal_mask = imresize(back_diagonal,[m,n]);


% saliency_gbvs.master_map_resized is this saliency map interpolated (bicubic) 
% to the resolution of the original image.

% ?????gbvs???itt???? http://www.vision.caltech.edu/~harel/share/gbvs.php
%?????
%out_itt = ittikochmap(img);
%saliency_gbvs.master_map
%figure;
%subplot(2, 3, 2); imshow(img);
%subplot(2, 3, 4); imshow(saliency_gbvs.master_map);
%subplot(2, 3, 6); imshow(out_itt.master_map);
%show_imgnmap(img,out_gbvs);


%RGB->HSV  ???H??????S?????V?
    try
        HSV = rgb2hsv(img);
        H = HSV(:, :, 1);
        S = HSV(:, :, 2);
        V = HSV(:, :, 3);

        double_V = double(V);
        %?????????
        % threshold = graythresh(double_V);
        % Mask = im2bw(double_V,threshold);
        % imshow(img)
        % imshow(diagonal_mask);
        double_circle_mask = double(circle_mask);
        double_diagonal_mask = double(diagonal_mask);
        double_back_diagonal_mask = double(back_diagonal_mask);

        threshold_circle = graythresh(double_circle_mask);
        threshold_diagonal = graythresh(double_diagonal_mask);
        threshold_back_diagonal = graythresh(double_back_diagonal_mask);
        
        c_Mask = im2bw(double_circle_mask,threshold_circle);
        d_Mask = im2bw(double_diagonal_mask,threshold_diagonal);
        bd_Mask = im2bw(double_back_diagonal_mask,threshold_back_diagonal);
        % imshow(c_Mask)
        %subplot(2, 1, 2); imshow(BW);
        %imwrite(Mask,'/Users/chenzian/863_image/threshold.png');

        c_SM_multiple = saliency_gbvs.master_map_resized.*c_Mask;
        
        c_SM_sum = sum(c_SM_multiple(:));
        c_S_sum = sum(saliency_gbvs.master_map_resized(:));
        c_RFA = c_SM_sum/c_S_sum;

        d_SM_multiple = saliency_gbvs.master_map_resized.*d_Mask;
        
        d_SM_sum = sum(d_SM_multiple(:));
        d_S_sum = sum(saliency_gbvs.master_map_resized(:));
        d_RFA = d_SM_sum/d_S_sum;

        bd_SM_multiple = saliency_gbvs.master_map_resized.*bd_Mask;
        bd_SM_sum = sum(bd_SM_multiple(:));
        bd_S_sum = sum(saliency_gbvs.master_map_resized(:));
        bd_RFA = bd_SM_sum/bd_S_sum;
    catch
        c_RFA = 0;
        d_RFA = 0;
        bd_RFA = 0;
    end