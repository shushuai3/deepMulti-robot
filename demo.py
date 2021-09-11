import cv2
import numpy as np
import tensorflow as tf
from locaNet import locaNet
from PIL import Image, ImageDraw, ImageFont
import config as cfg
import math

def distance(a, b):
    return math.sqrt(pow((a[0]-b[0]), 2) + pow((a[1]-b[1]), 2))
def clean_array2d(array, threshold):
    i = 0
    while(i<len(array)):
        j = i+1
        while(j<len(array)):
            dist = distance(array[i], array[j])
            if dist < threshold:
                array.pop(j)
            else:
                j = j+1
        i = i+1
    return array

def image_predict(image_path, model):
    if cfg.INPUT_CHANNEL == 3:
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    else:
        original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        original_image = original_image[..., np.newaxis]
    original_image = original_image.astype('float32')
    original_image = original_image/128 - 1
    image_data = original_image[np.newaxis, ...].astype(np.float32)
    conv = model.predict(image_data)
    conf = tf.sigmoid(conv[0, :, :, 1:2])
    # for i in range(28):
    #     print(np.round(np.array(conv[0, i, :, 0:1]).T, 0))
    pos_conf_above_threshold = np.argwhere(conf > 0.3)
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 26, encoding="unic")

    dist = 5
    list_pos = pos_conf_above_threshold.tolist()
    pos_conf_above_threshold = clean_array2d(list_pos, dist)

    for xy in pos_conf_above_threshold:
        print(xy[0:2])
        curH = (xy[0]-0.5)*8
        curW = (xy[1]+0.5)*8
        draw.ellipse((curW-4, curH-4, curW+4, curH+4), outline ='white', width=2)
        draw.ellipse((curW-7, curH-7, curW+7, curH+7), outline ='black', width=2)
        draw.text((curW-20, curH),"{:3.2f}m".format(tf.exp(conv[0, xy[0], xy[1], 0])),fill='white', stroke_fill='black', stroke_width=1, font=font)
    image.show()
    # image.save(image_path[-6]+image_path[-5]+'.png')

def pred_max_conf(image_path, model):
    if cfg.DATASET_FOLDER == 'synImgs':
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    else:
        original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        original_image = original_image[..., np.newaxis]
    original_image = original_image.astype('float32')
    original_image = original_image/128 - 1
    image_data = original_image[np.newaxis, ...].astype(np.float32)
    conv = model.predict(image_data)   
    conf = tf.sigmoid(conv[0, :, :, 1])
    xy = [np.argmax(conf)//40, np.argmax(conf)%40]
    d = tf.exp(conv[0, xy[0], xy[1], 0])
    # image = Image.open(image_path)
    # draw = ImageDraw.Draw(image)
    # draw.ellipse(((xy[0]-0.5)*8-5, (xy[1]-0.5)*8-5, (xy[0]-0.5)*8+5, (xy[1]-0.5)*8+5), outline ='white')
    # image.show()
    return [(xy[1]+0.5)*8, (xy[0]+0.5)*8, float(d)]

input_size   = [224, 320]
input_layer  = tf.keras.layers.Input([input_size[0], input_size[1], cfg.INPUT_CHANNEL])
feature_maps = locaNet(input_layer)
model = tf.keras.Model(input_layer, feature_maps)
model.load_weights("./output/locaNet")
model.summary()

## Figure in the paper
# image_predict("./dataset/synImgsMulti/0026.jpg", model)
# image_predict("./dataset/synImgsMulti/0037.jpg", model)
image_predict("./dataset/synImgs/0837.jpg", model) # sample also in AIdeck
# image_predict("./dataset/synImgs/0970.jpg", model)

## Figure in the paper
# lineAll = []
# y_err = []
# z_err = []
# d_err = []
# with open('dataset/synImgs/test.txt', 'r') as file:
#     for row in file:
#         lineAll.append(row.split())
# for line in lineAll:
#     imgPath = line[0]
#     y_p = float(line[2].split(',')[0])
#     z_p = float(line[2].split(',')[1])
#     d   = float(line[2].split(',')[2])/1000.0
#     predict = pred_max_conf(imgPath, model)
#     y_err.append(y_p - predict[0])
#     z_err.append(z_p - predict[1])
#     d_err.append(d   - predict[2])
# import matplotlib.pyplot as plt
# allData = [y_err, z_err]
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
# axes[0].violinplot(allData, showmeans=True, showmedians=True)
# axes[0].set_title('2D position error in image')
# axes[0].yaxis.grid(True)
# axes[0].set_xticks([y+1 for y in range(len(allData))])
# axes[0].set_ylabel('Position error in pixels')
# axes[0].set_xticklabels([r'$y_{p}$',r'$z_{p}$'])
# axes[1].violinplot([d_err], showmeans=True, showmedians=True)
# axes[1].set_title('Depth error')
# axes[1].yaxis.grid(True)
# axes[1].set_xticks([y+1 for y in range(len([d_err]))])
# axes[1].set_ylabel('Depth error in meters')
# axes[1].set_xticklabels([r'$d$'])
# fig.tight_layout(pad=3.0)
# plt.show()

# ## Figure position error
# from numpy.linalg import inv
# lineAll = []
# px_err = []
# py_err = []
# pz_err = []
# with open('dataset/synImgs/test.txt', 'r') as file:
#     for row in file:
#         lineAll.append(row.split())
# for line in lineAll:
#     imgPath = line[0]
#     predict = pred_max_conf(imgPath, model)
#     pI = np.array([[predict[0]], [predict[1]], [1]])
#     phi = float(line[1].split(',')[0])/180*3.1415
#     theta = -float(line[1].split(',')[1])/180*3.1415
#     RxInv = np.array([[1, 0, 0], [0, np.cos(phi), np.sin(phi)], [0, -np.sin(phi), np.cos(phi)]])
#     RyInv = np.array([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]])
#     Intrin = np.array([[185.14, 0, 169.54], [0, 185.13, 85.76], [0, 0, 1]])   
#     pC_TL = inv(Intrin)@pI*predict[2]
#     pC = inv(np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]))@pC_TL
#     pH = inv(RyInv@RxInv)@pC
#     pH_GT = np.array([[float(line[3].split(',')[0])], [float(line[3].split(',')[1])], [float(line[3].split(',')[2])]])   
#     px_err.append(pH[0,0] - pH_GT[0,0])
#     py_err.append(pH[1,0] - pH_GT[1,0])
#     pz_err.append(pH[2,0] - pH_GT[2,0])
# import matplotlib.pyplot as plt
# allData = [px_err, py_err, pz_err]
# fig, axe = plt.subplots(figsize=(9, 4))
# axe.violinplot(allData, showmeans=True, showmedians=True)
# # axe.set_title('2D position error in image')
# axe.yaxis.grid(True)
# axe.set_xticks([y+1 for y in range(len(allData))])
# axe.set_ylabel('3D position error in horizontal frame')
# axe.set_xticklabels([r'$y_{h}$',r'$z_{h}$',r'$x_{h}$'])
# plt.show()