'''
Generation of synthetic images for multi-robot relative localization
Specifics: variant attitude and position of both camera and robots

Author: Shushuai Li, MAVLab, TUDelft
'''
import bpy
import numpy as np
import random
import math
import os

# Configurations
random.seed(19910620) # random seed for replication
BGImgPath = 'background/' # path of background images
synImgsPath = 'synImgs/'
os.mkdir(synImgsPath) # Create a folder for saving images
fileBoxLabel = open(synImgsPath+'boxLabel.txt', 'w')
filePosLabel = open(synImgsPath+'posLabel.txt', 'w')
numsSynImgs = 980 # the number of synthetic images
maxRobot = 1 # the maximum number of robots (at least one)
maxRollPitch = math.radians(20) # maximum tilt angles -20~20 degree

# Initialization of blender
tree = bpy.context.scene.node_tree
robotDefault = bpy.data.objects['crazyflie']
camera = bpy.data.objects['Camera']
lamp = bpy.data.objects['Lamp']
RotCamInit2earth = np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]]) # rotation of initial camera coordinate to earth
BGImgNameList = os.listdir(BGImgPath)
BGImgNameList.sort()
#bpy.data.objects.remove(bpy.data.objects['crazyflie.001'])

def random_color_of_appearance():
    for i in range(8):
        bpy.context.object.active_material_index = i
        bpy.context.object.active_material.diffuse_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)

# Main loop
for numSynImgs in range(numsSynImgs):
    fileNameRendering = '%04d.jpg' % numSynImgs
    # Random rotation of camera
    rollCam  = random.uniform(-maxRollPitch, maxRollPitch)
    pitchCam = random.uniform(-maxRollPitch, maxRollPitch)
    camera.rotation_euler = np.matmul(RotCamInit2earth, np.array([rollCam, pitchCam, 0]).T)
    lamp.rotation_euler = np.matmul(RotCamInit2earth, np.array([rollCam, pitchCam, 0]).T)
    # Rotation from cameraInit to camera: roll-pitch (X-Y order) sequence
    rotCam2camInit = np.array([[np.cos(pitchCam), 0, np.sin(pitchCam)],
        [np.sin(rollCam)*np.sin(pitchCam), np.cos(rollCam), -np.sin(rollCam)*np.cos(pitchCam)],
        [-np.cos(rollCam)*np.sin(pitchCam), np.sin(rollCam), np.cos(rollCam)*np.cos(pitchCam)]])

    # Create multiple crazyflie objects
    numRobot = random.randint(1, maxRobot)
    robotList = [robotDefault]
    for i in range(numRobot - 1):
        robotNew = robotDefault.copy()
        bpy.context.collection.objects.link(robotNew)
        robotList.append(robotNew)

    # Random position and rotation of all robots; position in camera coordinate
    posHistory = []
    filePosLabel.write('./dataset/' + synImgsPath + fileNameRendering + ' {},{}'.format(rollCam, pitchCam))
    # random_color_of_appearance() # comment cause network size is too small for too many appearances
    for i in range(numRobot):
        xCam2robot = random.uniform(0.2, 2) # robot's x position [m] in the camera coordinate
        yCam2robot = random.uniform(-1.1, 1.1)*xCam2robot # make sure the robot is in the camera view
        zCam2robot = random.uniform(-0.85, 0.85)*xCam2robot
        rollRobot  = random.uniform(-maxRollPitch, maxRollPitch)
        pitchRobot = random.uniform(-maxRollPitch, maxRollPitch)
        yawRobot   = math.radians(random.uniform(0,360)) # random yaw 0~360 degree
        xInCamInit, yInCamInit, zInCamInit = np.matmul(rotCam2camInit, np.array([xCam2robot, yCam2robot, zCam2robot]).T)
        xyzInEarth = np.matmul(RotCamInit2earth, np.array([xInCamInit, yInCamInit, zInCamInit]).T)
        attInEarth = np.matmul(RotCamInit2earth, np.array([rollRobot, pitchRobot, yawRobot]).T)
        robotList[i].location = 500*xyzInEarth # 500 means 1m
        robotList[i].rotation_euler = attInEarth
        posHistory.append([500*xyzInEarth[0], 500*xyzInEarth[1], 500*xyzInEarth[2], attInEarth[0], attInEarth[1], attInEarth[2]])
        filePosLabel.write(' {},{},{},{},{},{}'.format(xCam2robot, yCam2robot, zCam2robot, rollRobot, pitchRobot, yawRobot))
    filePosLabel.write('\n')

    # Render image
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    tree.nodes['Image'].image = bpy.data.images.load(BGImgPath + BGImgNameList[numSynImgs])
    bpy.data.scenes["Scene"].render.filepath = synImgsPath + fileNameRendering
    bpy.ops.render.render(write_still=True)
    
    # Calculate the bounding box of each robot
    fileBoxLabel.write('./dataset/' + synImgsPath + fileNameRendering)
    for i in range(numRobot):
        for j in range(numRobot):
            robotList[j].location[1] = 10*500 # move all robots out of camera's view
        robotList[i].location = posHistory[i][0:3]
        robotList[i].rotation_euler = posHistory[i][3:6]
        # Render each robot without background
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.data.scenes["Scene"].render.filepath = 'tmp.png'
        bpy.ops.render.render(write_still=True)

        load_img = bpy.data.images.load('tmp.png', check_existing=False)
        width, height = load_img.size
        pixels = list(load_img.pixels)
        pixRedListNon0 = [int(pixels[ipx]*1000) for ipx in range(0, len(pixels), 4)]
        indexNon0 = [i for i, e in enumerate(pixRedListNon0) if e != 250]
        wNon0 = [i%width for i in indexNon0]
        hNon0 = [height-int(i/width) for i in indexNon0]   
        bbox = [min(wNon0), min(hNon0), max(wNon0), max(hNon0)]
        print(bbox)
        fileBoxLabel.write(' {},{},{},{},{}'.format(bbox[0], bbox[1], bbox[2], bbox[3], 0))
    fileBoxLabel.write('\n')
    
    # Remove all copy objects
    for i in range(1, numRobot):
        bpy.data.objects.remove(robotList[i])
    print("numSynImgs={}".format(numSynImgs))

os.remove('tmp.png')
fileBoxLabel.close()
filePosLabel.close()
existed_objects = bpy.data.objects
for i in existed_objects:
    print(i)
