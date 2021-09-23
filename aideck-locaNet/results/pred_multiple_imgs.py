# require main.c with WriteImageToFile
# make clean all once at first
# read images in a folder and predict on AIdeck

import os
from tkinter import image_names
import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image

# prediction on AIdeck
# fileNames = []
# for name in glob.glob("../dataset/aideck-dataset/imageStorage/imagesH2C/*.ppm"):
#     fileNames.append(name)
# fileNames.sort()
# destFile = 'images/0026.ppm'
# for origFile in fileNames:
#     # copy a image to the images folder for aideck prediction
#     # origFile = '../dataset/aideck-dataset/imageStorage/imagesH2C/img00000.ppm'
#     os.system('cp {} {}'.format(origFile, destFile))
#     os.system('make run io=host')
#     depthFile = 'images/dep'+origFile[-9:]
#     os.system('cp {} {}'.format('img_depth.ppm', depthFile))
#     depthFile = 'images/pos'+origFile[-9:]
#     os.system('cp {} {}'.format('img_position.ppm', depthFile))
# organize the folder of the output files

# fileNames = []
# for name in glob.glob("images/depthH2C/*.ppm"):
#     fileNames.append(name)
# fileNames.sort()
# for origFile in fileNames:
#     img = Image.open(origFile)
#     sequence_of_pixels = img.getdata()
#     list_of_pixels = list(sequence_of_pixels)
#     x = np.reshape(list_of_pixels, (28, 40))
#     plt.imshow(x)
#     plt.savefig('images/dH2C/img' + origFile[-9:-4] + '.png')

fileNames = []
for name in glob.glob("images/posH2C/*.ppm"):
    fileNames.append(name)
fileNames.sort()
for origFile in fileNames:
    img = Image.open(origFile)
    sequence_of_pixels = img.getdata()
    list_of_pixels = list(sequence_of_pixels)
    x = np.reshape(list_of_pixels, (28, 40))
    plt.imshow(x)
    plt.savefig('images/pH2C/img' + origFile[-9:-4] + '.png')

# animate -delay 10 *.ppm