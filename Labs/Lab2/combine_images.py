import cv2
import numpy
import os


def combine_images(input_folder, output_path, ext=".png", images_of_interest=None, shape=None):
    #pathname = os.path.join(input_folder, "*" + ext)
    # files = glob.glob(pathname)
    files = [os.path.join(input_folder,f) for f in os.listdir(input_folder) if f[-len(ext):]==ext and "combined" not in f]
    images = [cv2.imread(img) for img in files]
    if shape is None:
        shape = [1, len(images)]


    height = max(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = numpy.ones((height*shape[0], width*shape[1], 3))*255

    i = 0
    j = 0
    y = 0
    x = 0
    for image in images:
        h, w, d = image.shape
        w = width
        h = height

        output[y:y+h,x:x + w] = image
        x += w
        j += 1
        if j >= shape[1]: # go to next row
            i += 1
            j = 0
            x = 0
            y += h # assumes constant height, else use max
        if i >= shape[0]: # no more room
            break


    cv2.imwrite(output_path, output)

def combine_all(path):
    for folder in os.listdir(path):
        full_path = os.path.join(path, folder)
        print(full_path)
        images = len(os.listdir(full_path))
        if images in range(0,3):
            shape = [1,2]
        elif images in range(3,4):
            shape = [2,2]
        elif images in range(4,7):
            shape = [2,3]
        elif images in range(7,10):
            shape = [3,3]
        elif images in range(10,13):
            shape = [3,4]
        elif images in range(14,17):
            shape = [4,4]
        elif images in range(17,20):
            shape = [4,5]
        combine_images(full_path, output_path=os.path.join(full_path,"combined.png"), shape=shape)

if __name__=="__main__":
    if False:
        folder = r"D:\OneDrive\Documents\Graduate School\2018.4\CS 670\Labs\Labs\Lab2\graphs\PD,0.95,30,wt=[0.88, 0.01, 0.05, 0.05],random,['AC', 'AD', 'TFT', 'nTFT']"
        shape = [4,3]
        combine_images(folder, os.path.join(folder,"combined.png"), shape=shape)

        folder = r"D:\OneDrive\Documents\Graduate School\2018.4\CS 670\Labs\Labs\Lab2\graphs\PD,0.95,30,wt=[0.6, 0.05, 0.3, 0.05],random,['AC', 'AD', 'TFT', 'nTFT']"
        shape = [4,4]
        combine_images(folder, os.path.join(folder,"combined.png"), shape=shape)

        folder = r"D:\OneDrive\Documents\Graduate School\2018.4\CS 670\Labs\Labs\Lab2\graphs\antinephi"
        shape = [4,4]
        combine_images(folder, os.path.join(folder,"combined.png"), shape=shape)

    combine_all(r"D:\OneDrive\Documents\Graduate School\2018.4\CS 670\Labs\Labs\Lab2\graphs")