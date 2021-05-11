# locaNet - Monocular Multi-robot Relative Localization with Deep Neural Networks

This project proposes a locaNet for multi-robot localization by predicting the pixel position of the robot center and its distance from the camera, which can be transformed to inertial 3D relative positions using the intrinsic parameter. The implementation contains several code projects: 1) Blender code for synthetic dataset generation; 2) TensorFlow-based network of the locaNet and training; 3) Onboard deep network code on the AIdeck; 4) Quadrotor control code based on Crazyflie firmware.

## Contents

    .
    ├── locaNet                 # neural network, training, and testing
    ├── dataset                 # synthetic and real-world flight dataset
    ├── locaAIdeck              # deep network on the AI edge chip - GAP8
    ├── crazyflie-firmware      # autopilot code of quadrotors
    ├── LICENSE
    └── README.md

<!-- <p align="center">
  <img width="400" height="260" src="./plot.png">
</p> -->

Paper: [PDF on arXiv](abc).

Video: [Real-world flight on Youtube](abc).

## Requirements

 - locaNet & locaAIdeck (Python 3.6, pip=20.1.1, tensorflow==2.1.2, h5py==2.10.0)
 - dataset (Blender, numpy, csv, statistics)

## Quick start - image demo
    $ git clone https://github.com/shushuai3/deepMulti-robot.git
    

<!-- ## Quick start - running on robot
    $ python3 main_simulation.py -->