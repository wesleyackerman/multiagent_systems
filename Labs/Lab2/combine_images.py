import cv2
import numpy
import glob
import os


def combine_images(input_folder, output_path, ext=".png", images_of_interest=None, shape=None):
    pathname = os.path.join(input_folder, "*" + ext)
    images = [cv2.imread(img) for img in glob.glob(pathname)]

    if shape is None:
        shape = [1, len(images)]

    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = numpy.zeros((height, width, 3))

    i = 0
    j = 0
    y = 0
    x = 0
    for image in images:
        h, w, d = image.shape
        print(output.shape)
        output[0:h,x:x + w] = image
        x += w
        j += 1
        if i > shape[0]:
            break
        elif j > shape[1]: # next row
            i +=1
            j = 0
            x = 0
            y += h # assumes constant height, else use max


    cv2.imwrite(output_path, output)

if __name__=="__main__":
    folders = [r"D:\OneDrive\Documents\Graduate School\2018.4\CS 670\Labs\Labs\Lab2\graphs\BS,0.95,30,wt=None,diagonal"]
    for folder in folders:
        combine_images(folder, os.path.join(folder,"combined.png"))