# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio

# name of the input file
# imname = 'cathedral.jpg'
imname = 'melons.tif'


# read in the image
im = skio.imread(imname)

# convert to double (might want to do this later on to save memory)    
im = sk.img_as_float(im)


# compute the height of each part (just 1/3 of total)
height = np.floor(im.shape[0] / 3.0).astype(int)

# separate color channels
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]
# print(r.dtype)


def align_l2(a, b):
    # a =(a - np.mean(a)) / np.std(a)
    # b =(b - np.mean(b))/ np.std(b)
    best=np.inf
    disp = (0, 0)
    x_a, y_a =a.shape
    x_b, y_b =b.shape
    
    for i in range(-15, 16):
        for j in range(-15, 16):
            shif_b= np.roll(b,shift=i, axis=0)
            shift_b =np.roll(shif_b, shift=j, axis=1)
            x_min = min(x_a, x_b)
            y_min = min(y_a, y_b)
            a_block =a[:x_min, :y_min]
            b_block = shift_b[:x_min, :y_min]
            score = np.linalg.norm(a_block - b_block)
            # a_norm=a_block/np.linalg.norm(a_block)
            # b_nomr= b_block/np.linalg.norm(b_block)
            # score= np.sum(a_norm*b_nomr)
            if score < best:
                best = score
                disp = (-i, -j)
    print("DSP", disp)
    return disp

def canny(a):
    a_equal= sk.exposure.equalize_hist(a)
    a_canny= sk.feature.canny(a_equal, 2.5)
    return a_canny

def phase(a,b):
    a = sk.exposure.equalize_hist(a)
    b = sk.exposure.equalize_hist(b)

    shift, error, diffphase = sk.registration.phase_cross_correlation(a, b)
    x,y=shift
    x=int(x)
    y=int(y)
    return (-x,-y)


def image_pyr (a,b):
    # represents the image at multiple scales (usually scaled by a factor of 2) 
    # and the processing is done sequentially starting from the coarsest scale 
    # (smallest image) and going down the pyramid, updating your estimate as you go. 
    # It is very easy to implement by adding recursive calls to your original single-scale 
    # implementation
    print("original",a.shape)
    x_curr =0
    y_curr=0
    min_size =300
    if a.shape[0] >min_size or a.shape[1]>min_size:
        print("resize")
        a_resc = sk.transform.rescale(a, 0.5, anti_aliasing=True)
        b_resc = sk.transform.rescale(b, 0.5, anti_aliasing=True)
        x_curr,y_curr=image_pyr(a_resc,b_resc)
        print("REcieved", (x_curr,y_curr))
        x_curr=x_curr*2
        y_curr=y_curr*2
        shift_a= np.roll(a,shift=(x_curr,y_curr), axis=(0,1))
        x,y= phase(shift_a, b)
        x_curr+=x
        y_curr+=y
        print("Recursive call",(x_curr,y_curr))

    else:
        print("A LEN",a.shape)
        x_curr =0
        y_curr=0
        shift_a=a
        x,y= phase(shift_a, b)
        x_curr+=x
        y_curr+=y
    return (x_curr,y_curr)

    
def image_pyr_canny (a,b):
    # represents the image at multiple scales (usually scaled by a factor of 2) 
    # and the processing is done sequentially starting from the coarsest scale 
    # (smallest image) and going down the pyramid, updating your estimate as you go. 
    # It is very easy to implement by adding recursive calls to your original single-scale 
    # implementation
    a= canny(a)
    b=canny(b)
    print("original",a.shape)
    x_curr =0
    y_curr=0
    min_size =300
    if a.shape[0] >min_size or a.shape[1]>min_size:
        print("resize")
        a_resc = sk.transform.rescale(a, 0.5, anti_aliasing=False)
        b_resc = sk.transform.rescale(b, 0.5, anti_aliasing=False)
        x_curr,y_curr=image_pyr_canny(a_resc,b_resc)
        print("REcieved", (x_curr,y_curr))
        x_curr=x_curr*2
        y_curr=y_curr*2
        shift_a= np.roll(a,shift=(x_curr,y_curr), axis=(0,1))
        x,y= phase(shift_a, b)
        x_curr+=x
        y_curr+=y
        print("Recursive call",(x_curr,y_curr))

    else:
        print("A LEN",a.shape)
        x_curr =0
        y_curr=0
        shift_a=a
        x,y= phase(shift_a, b)
        x_curr+=x
        y_curr+=y
    return (x_curr,y_curr)


    #scale down until hit 256?
    #lowest level align, then realign
    

ar = image_pyr_canny(r,b)
ag = image_pyr_canny(g, b)

g_align = np.roll(np.roll(g, shift=ag[0], axis=0), shift=ag[1], axis=1)
r_align = np.roll(np.roll(r, shift=ar[0], axis=0), shift=ar[1], axis=1)
# create a color image
im_out = np.dstack([r_align, g_align, b])
# has to normalize it
# when saving have to convert data type, unsigned 8 bit int
# save the image
fname = 'catherdralout.jpg'
im_out = (im_out * 255).astype(np.uint8)
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()


# histogram equilization, and do adaptive, or do opencv edge detection 
# use skimage.canny
            


# (176,7) (83,4)

