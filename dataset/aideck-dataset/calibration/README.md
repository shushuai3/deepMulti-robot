# Calibration
There are several steps to calibrate the intrinsic parameters of the AIdeck camera

 - Print the Checkerboard image in a A4 page
 - Keep the camera fixed
 - Replace 'start_storing' with 1 in test.c file
 - Uncomment the three lines after 'start_storing'
 - Run: make clean all write=1 run io=host
 - Change the attitude and pos of the A4 page
 - Images will be saved in 'images' folder
 - Move them in the 'calibration' folder
 - Open matlab and navigate to the 'calibration' folder
 - Open Camera Calibrator app and select the sample images