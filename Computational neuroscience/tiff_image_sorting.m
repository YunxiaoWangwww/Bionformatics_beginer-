ims = imfinfo('cell.tif'); %get the informaton of the cell image 
%read the image -> as only one image is loaded
imstack = imread('cell.tif');
%calculate the maximum intensity in the third dimension of the imstack ->
%convert a multi-dimensional image into an one-dimensional image 
imm = max(imstack,[],3);
%convert the image to a grayscale that has a range of [0,1]
img = mat2gray(imm);
%imtool allows the interaction with the image 
imtool(img)
%sharpen the image by subtracting a blurred version of the image 
ims = imsharpen(img);
%view the image 
imtool(ims)
%output te threshold for image segmentation automatically
threshold = graythresh(ims)
%segmentation -> everything above the threshold becomes 1 (white) and below
%will be 0 (black)
imthresholded = im2bw(ims,threshold);
%plot the original image and the sharpened image 
subplot(1,2,1),imshow(img),subplot(1,2,2),imshow(imthresholded)
%fill the gap or the wholes (some small white parts are surronded by black)
imfilled = imfill(imthresholded,'holes');
imtool(imfilled)
%enumerate the filled objects as a matrix 
imobjs = bwlabel(imfilled);
%convert the matrix into an RGB image with colors 
labeledim = label2rgb(imobjs);
imshow(labeledim )
%regionprops identify lots of properties of the sharpened filled grey image
improps = regionprops(imobjs,'all')
%the SubarrayIdx allow direct extraction of the subimages 
%firstObj will be an array with row number as SubarrayIdx{1} and column
%number as SubarrayIdx{2} -> this is the parameters of the first cell ->
%according to this index, find the corresponding subfraction in the
%original img grey image 
firsObj = img(improps(1).SubarrayIdx{1},improps(1).SubarrayIdx{2});
imshow(firsObj)
imsize = size(firsObj);
%plot the central profile of the first cell -> draw a midline in the width  
plot(firsObj(round(imsize(1)/2),:),'k.','MarkerSize',6)
%plot the whole cell (for the first cell) as a surface 
surf(firsObj,'FaceColor','interp','EdgeColor','interp')
%nobjs returns number of cells in this tif figure
nobjs = length(improps);
nrows = round(sqrt(nobjs));
ncols = ceil(sqrt(nobjs));
%plot the surf for each cell with area greater than 5 in the tif figure
for jj = 1:nobjs
    if improps(jj).Area >= 5
        obj = img(improps(jj).SubarrayIdx{1},improps(jj).SubarrayIdx{2});
        subplot(nrows,ncols,jj),surf(obj,'FaceColor','interp','EdgeColor','interp')
    end
end
          
     
          
         
