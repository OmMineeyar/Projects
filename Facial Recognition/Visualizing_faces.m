clear all;
clc;
folder_path = 'C:\Users\ommin\OneDrive\Desktop\Jupyter Notebook\CH5440\assn3\assign3_2024\yalefacespng';

%% Importing images
image_size = [243, 320]; % height x width

num_images_per_subject = 6;
num_subjects = 15;

subject_arrays = cell(num_subjects, 1);

all_images = [];

norm_array = cell(num_subjects, 1);

for subject = 1:num_subjects
    subject_array = cell(num_images_per_subject, 1);
    
    for image_idx = 1:num_images_per_subject
        filename = sprintf('s%02d%s.png', subject, getImageSuffix(image_idx));
        
        img = imread(fullfile(folder_path, filename));
        
        img_vector = img(:);
        
        col_name = filename(1:end-4); % Remove extension
        subject_array{image_idx} = struct('name', col_name, 'vector', img_vector);
        
        all_images = [all_images, img_vector];
    end    
    subject_arrays{subject} = subject_array;
end
%% Part A

all_images=double(all_images);
norm_mat=zeros([15 90]);
for j=1:15
    for i=1:90
        norm_mat(j,i)=norm(all_images(:,i)-all_images(:,6*j));
    end
end
%fprintf("Image Number       Identification\n");
c1=0;
for i=1:90
    poosible_norms = norm_mat(:, i);
    est_subject = find(poosible_norms == min(poosible_norms, [], "all"));
    true_subject = floor((i-1)/6) + 1;
    if est_subject == true_subject
        %fprintf("   %d                  YES\n",i);
        c1 = c1 + 1;
    else
        %fprintf("   %d                   NO\n",i);
    end
end
%ssbtracted 15 because ofcourse the original image will recognize itself
percentage_recognition1=c1-15/(90-15)*100;
%fprintf("Percentage recognition for test using sample image %f\n",percentage_recognition1)
figure;
pca=zeros([15 90]);
%% Calculating PCs and visualizing the pc images
for j=1:15
    first_image_set=[all_images(:,1+6*(j-1):6*j)];
    for i=1:77760
        mean_arr(i)=mean(first_image_set(i,:));
        mean_image(i,:)=[first_image_set(i,:)-mean(first_image_set(i,:))];
    end
    cov_mat = cov(mean_image);
    [v1,d1]=eig(cov_mat);
    p11=mean_image*v1(:,6);
    p22=mean_image*v1(:,5);
    norm_mat_1st=[];
    for i=1:77760
        re_image_1(j,i)=p11(i)+mean_arr(i);
        re_image_2(j,i)=p22(i)+mean_arr(i);
    end
    re_image_1(j,:)=uint8(re_image_1(j,:));
    re_image_2(j,:)=uint8(re_image_2(j,:));
    re_image_1(j,:)=double(re_image_1(j,:));
    re_image_2(j,:)=double(re_image_2(j,:));
    reimage1=uint8(re_image_1(j,:));
    reimage2=uint8(re_image_2(j,:));
    for i=1:90
        pca1(j,i)=norm(all_images(:,i)-re_image_1(j,:)');
        pca2(j,i)=norm(all_images(:,i)-re_image_2(j,:)');
    end
    reimage1=reshape(reimage1,image_size);
    reimage2=reshape(reimage2,image_size);
    subplot(8,4,2*j-1)
    imshow(reimage1);
    subplot(8,4,2*j)
    imshow(reimage2);
end
%% part B
%fprintf("Image Number       Identification\n");
c2=0;
for i = 1:90
    poosible_norms = pca1(:, i);
    est_subject = find(poosible_norms == min(poosible_norms, [], "all"));
    true_subject = floor((i-1)/6) + 1;
    if est_subject == true_subject
        %fprintf("   %d                 YES\n",i);
        c2 = c2 + 1;
    else
        %fprintf("   %d                  NO\n",i);
    end
end
percentage_recognition2=c2/90*100;
%fprintf("Percentage recognition for test using one PC %f\n",percentage_recognition2)

%% Part C 
%fprintf("Image Number       Identification\n")
c3=0;
all_pca=[pca1;pca2];
for i = 1:90
    poosible_norms = all_pca(:, i);
    est_subject = find(poosible_norms == min(poosible_norms, [], "all"));
    true_subject = floor((i-1)/6) + 1;
    if est_subject == true_subject || est_subject-15==true_subject
        %fprintf("   %d                 YES\n",i);
        c3 = c3 + 1;
    else
        %fprintf("   %d                  NO\n",i);
    end
end
percentage_recognition3=c3/90*100;
%fprintf("Percentage recognition for test combining both the PCAs is %f\n",percentage_recognition3)
% fprintf('%d%d',c,c1);
%% Comparison
%f=table(percentage_recognition1,percentage_recognition2,percentage_recognition3);
%disp(f);


%%
function suffix = getImageSuffix(image_idx)
    switch image_idx
        case 1
            suffix = 'cl';
        case 2
            suffix = 'glass';
        case 3
            suffix = 'happy';
        case 4
            suffix = 'll';
        case 5
            suffix = 'ng';
        case 6
            suffix = 'norm';
        otherwise
            error('Invalid image index.');
    end
end