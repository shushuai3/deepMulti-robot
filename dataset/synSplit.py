'''
Split the synthetic dataset for training and validation
'''
from PIL import Image, ImageDraw

# Read the relative information.
# Dataset format: img_name roll,pitch xToCam,yToCam,zToCam,roll,pitch,yaw
attPos = []
with open('dataset/synImgs/posLabel.txt', 'r') as file:
    for row in file:
        attPos.append(row.split())

## Projection from relative position to pixel position (imgSize: 320x224)
## Equation: xToCam/focal = yToCam/yInImg = zToCam/zInImg
# picNum = 0
# xToCam = float(attPos[picNum][2].split(',')[0])
# yToCam = float(attPos[picNum][2].split(',')[1])
# zToCam = float(attPos[picNum][2].split(',')[2])
# print(yToCam, zToCam)
# yInImg = -yToCam/xToCam*122 + 160
# zInImg = -zToCam/xToCam*122 + 112
# image = Image.open(attPos[picNum][0])
# draw = ImageDraw.Draw(image)
# draw.ellipse((yInImg-5, zInImg-5, yInImg+5, zInImg+5), outline ='blue')
# image.show()

## New format: img_name roll,pitch yInImg,zInImg,xToCam,class (...)
def writeLine(fileObj, attPos, line):
    dataLine = attPos[line][0] + ' '       # file name
    dataLine += attPos[line][1] + ' '      # roll & pitch
    xToCam = float(attPos[line][2].split(',')[0])
    yToCam = float(attPos[line][2].split(',')[1])
    zToCam = float(attPos[line][2].split(',')[2])
    yInImg = round(-yToCam/xToCam*122 + 162) # xToCam/focal = yToCam/yInImg
    zInImg = round(-zToCam/xToCam*122 + 122) # xToCam/focal = zToCam/zInImg
    if zInImg >= 224:
        zInImg = 223 # Avoid excess of index
    dataLine += str(yInImg) + ',' + str(zInImg) + ',' + str(round(xToCam*1000)) # m->mm
    dataLine += ',' + '0' + '\n' # add class
    fileTmp.write(dataLine)

## Create files
numImgTrain = round(0.8*len(attPos))
fileTmp = open('dataset/synImgs/synTrain.txt', 'w')
for line in range(0, numImgTrain):
    writeLine(fileTmp, attPos, line)
fileTmp.close()
fileTmp = open('dataset/synImgs/synTest.txt', 'w')
for line in range(numImgTrain, len(attPos)):
    writeLine(fileTmp, attPos, line)
fileTmp.close()