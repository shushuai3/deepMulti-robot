# Dataset

In this folder, synthetic datasets and real-world datasets are presented. If you like to render synthetic images by yourself, the following is the tutorial.

## Blender for rendering synthetic images
 - Installation of Blender: sudo snap install blender --classic
 - Download background images (background.zip) from https://github.com/shushuai3/deepMulti-robot/releases/tag/img_background
 - Extract the image files to 'dataset/background'
 - In terminal, go into 'dataset' folder and run Blender
 - Open the file 'synthetic.blend' in Blender
 - Click on 'Scripting->Run Script' in blender. You will get 1000 synthetic images and the box labels
 - Run 'synSplit.py' to get the final label files of 'synTrain.txt' and 'synTest.txt'
 - Tips: remember to click on 'crazyflie' in Scene Collection if you want to change the appearance