%identify how many cells in each tif file
files = dir('*.tif'); %extract all files terminated with a tif
for ii = 1:length(files)
    iminfo = imfinfo(files(ii).name);
      for jj = 1:length(iminfo)
        imstack = imread(files(ii).name);
      end
    imm = max(imstack,[],3);
    img = mat2gray(imm);
    
    % median filtering to remove noise
    img = medfilt2(img);
    % sharpen the image
    img = imsharpen(img);
    threshold = graythresh(img);
    %return either 1 or 0 as logics
    imbw = im2bw(img,threshold);
    %identify the object as numbers 
    imobjs = bwlabel(imbw);
    imshow(imobjs)
    
    improps = regionprops(imobjs,'all');
    %number of cells identified will be all stroed in the regionprops as a
    %struct file -> eg. if it is a 232x1 struct, there will be 232 cells 
    ncells = length(improps);
    sprintf('This image contains %d cells', ncells) 
end
