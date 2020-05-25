import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage import data, measure
import matplotlib.pyplot as plt
from skimage.util import invert
from scipy import ndimage


def RemoveConnectedComponent(img, threshold):
    label_img, cc_num = measure.label(img, return_num=True, connectivity=2)
    for i in range(1, cc_num+1):
        x = np.argwhere(label_img == i)
        if len(x) <= threshold:
            for i in x:
                img[i[0], i[1]] = 0
    return img


def Nbhd(I, x, y):

    n = 0
    (rows, cols) = I.shape
    # print(rows,cols)
    if ((x-1) >= 1 and (y-1) >= 1 and (x+1) < rows and (y+1) < cols):
        if(I[x-1, y-1] == 0 and I[x-1, y+1] == 0 and I[x+1, y+1] == 0 and I[x+1, y-1] == 0):
            if I[x+1, y] == 1:
                n = n+1

            if I[x, y+1] == 1:
                n = n+1

            if I[x, y-1] == 1:
                n = n+1
            if I[x-1, y] == 1:
                n = n+1
        else:
            if I[x-1, y-1] == 1:
                n = n+1

            if I[x-1, y+1] == 1:
                n = n+1

            if I[x+1, y-1] == 1:
                n = n+1

            if I[x+1, y+1] == 1:
                n = n+1

            if I[x+1, y] == 1:
                n = n+1
            if I[x, y+1] == 1:
                n = n+1

            if I[x, y-1] == 1:
                n = n+1
            if I[x-1, y] == 1:
                n = n+1
    return n

# def RemoveTail(input , threshold):
#   In = input
#   x , y = In.shape
#   print(x , y)
#   for i in range(1 , x):
#       for j in range(1 , y):
#           print(i , j)
#           if In[i,j] == 1:
#               N = Nbhd(In , i , j)
#               if(N>2):
#                   print(In[i , j])
#                   In[i,j] = 0
#                   In = RemoveConnectedComponent(In , threshold)
#                   In[i , j] = 1
#   return In


def RemoveTail(input, threshold):
    In = input
    x, y = In.shape
    m = []
    for i in range(1, x):
        for j in range(1, y):
            if In[i, j] == 1:
                N = Nbhd(In, i, j)
                if(N > 2):
                    m.append([i, j])
                    In[i, j] = 0

    In = RemoveConnectedComponent(In, threshold)
    # print(m)
    for x in m:
        In[x[0], x[1]] = 1
        N = Nbhd(In, i, j)
        if(N < 2):
            In[x[0], x[1]] = 0
    return In



cap = cv2.VideoCapture('walking.avi')

while cap.isOpened():

    image = cap.read()[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_delta = cv2.threshold(
        gray, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Below is the documentation code for skeletonise
    # Invert the horse image

    image = invert(thresh_delta)
    # print(image)
    # cv2.imshow('thresh_delta' , thresh_delta)
    # cv2.waitKey()
    im_bool = (image == 255)
    # print(im_bool)
    # perform skeletonization
    skeleton = skeletonize(im_bool, method='lee')
    # print((skeleton))
    # Puring
    skeleton_bool = (skeleton == 255)
    threshold = 35
    img = RemoveTail(skeleton_bool, threshold)
    # print(typeof(img))
    # display results
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 4),
                             sharex=True, sharey=True)

    ax = axes.ravel()

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].axis('off')
    ax[0].set_title('original', fontsize=20)

    ax[1].imshow(skeleton, cmap=plt.cm.gray)
    ax[1].axis('off')
    ax[1].set_title('skeleton', fontsize=20)

    ax[2].imshow(img, cmap=plt.cm.gray)
    ax[2].axis('off')
    ax[2].set_title('purned', fontsize=20)

    fig.tight_layout()
    plt.show()
    # cv2.imshow('skeleton' , skeleton)
    key = cv2.waitKey(1)
    if key == 13:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
