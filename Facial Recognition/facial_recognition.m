clear;
clc;
close all

table = struct2table(dir("yalefacespng\"));
table = table.name(3:92);

matrix = zeros(243,320,90);
image_matrix = zeros(77760,90);

for i=1:90
    matrix(:,:,i) = imread('yalefacespng\' + string(table(i)));
    image_matrix(:,i) = reshape(matrix(:,:,i),77760,1);
end
%% Part a

count=0;

for k=1:15
    min_norm = []; index=[];
    for j=1:90
        euc_distance = norm(image_matrix(:,j)-image_matrix(:,6*k));   % Calculating Euclidean distance between each image and normal images

        if size(min_norm) < 6                        % Finding the index of the 6 images with least norm
            min_norm = [min_norm euc_distance];
            index = [index j];
        elseif euc_distance < max(min_norm)
            [M, I] = max(min_norm);
            min_norm(I) = []; index(I)=[];
            min_norm = [min_norm euc_distance];
            index = [index j];
        end
    end

    Image_index = index'; Euclidean_dist = min_norm';

    for t=1:6
        if  (6*k-5 <= Image_index(t)) && (Image_index(t) <= 6*k)    % Counting the number of images that were identified correctly
            count = count+1;
        end
    end
end

fprintf('No. of images identified correctly = %.f\n',count)

clear i j k I

%% Part b

database1 = []; database2=[];

for i=1:15
    Z = image_matrix(:,6*i-5:6*i);        % Extracting 6 images corresponding to each subject
    Z_s = Z - mean(Z(:,1:6));
    covar = (Z_s'*Z_s)/77760;             % Finding covariance matrix

    [V,D] = eig(covar);                   % Eigenvalue decomposition

    PC1 = Z*(V(:,6).^2);                  % First PC corresponds to the last eigenvector in V
    database1 = [database1 PC1];          % Storing the first representative images for each subject in database1

    PC2 = Z*(V(:,5).^2);                  % Second PC comes from second last eigenvector
    database2 = [database2 PC2];          % Storing the second representative images for each subject in database2
end

count_new = 0;

for i=1:90
    Distance_with_representative_image = [];
    for j=1:15
        euc_distance = norm(image_matrix(:,i)-database1(:,j));   % Calculating norm with each representative image in database1
        Distance_with_representative_image = [Distance_with_representative_image euc_distance];
    end

    [M,I] = min(Distance_with_representative_image);    % Finding the index corresponding to minimum norm

    if (6*I-5<=i) && (i<=6*I)
        count_new = count_new + 1;                      % Counting the number of correctly classified images
    end

end

fprintf('No. of images correctly classified using one representative image = %.f \n',count_new)

%% Part c

count_new_2 = 0;

for i=1:90
    Distance_with_representative_image_1 = [];  Distance_with_representative_image_2 = [];

    for j=1:15
        euc_distance_1 = norm(image_matrix(:,i)-database1(:,j));   % Calculating norm with first representative images
        Distance_with_representative_image_1 = [Distance_with_representative_image_1 euc_distance_1];
    end

    [M1,I1] = min(Distance_with_representative_image_1);

    for j=1:15
        euc_distance_2 = norm(image_matrix(:,i)-database2(:,j));   % Calculating norm with second representative images
        Distance_with_representative_image_2 = [Distance_with_representative_image_2 euc_distance_2];
    end

    [M2,I2] = min(Distance_with_representative_image_2);

    if (6*I1-5<=i) && (i<=6*I1)             % Counting the number of correctly classified images
        count_new_2 = count_new_2 + 1;      % If an image isn't classified correctly using database1, 
    elseif (6*I2-5<=i) && (i<=6*I2)         % then second representative image is used.
        count_new_2 = count_new_2 + 1;
    end

end

fprintf('No. of images correctly classified using two representative images = %.f \n',count_new_2)

