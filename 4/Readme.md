get_harris_corners ->gets the harris corners
adaptive_non_maximal_suppression-> Does ANMS on the points using the coordinates. Pass the harris points for the specific coordinates in as well as the coordinate points Transposed. Then also pass in the amount of ANMS points you want. With this algorithm choose a lot of AMNS points so that the feature matching will be able to get enough points with a threshold of about 0.6.
feature_descr-> gets the features for an image using an image with only one of the color layers, and passing in the ANMS points as well
feature_match-> matches the features using the list of feature descriptors and using a threshold to find the matches
ransac-> will get the ransac points 
warp_image-> gets the final mosaic using the 2 images, and the ransac points
auto_pano-> put in 2 images and get the final panoramic using all the techniques implemented above
