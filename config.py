DATASET_FOLDER = 'synImgs'
# DATASET_FOLDER = 'aideck-dataset/imageStorage'
INPUT_CHANNEL = 3 # RGB: 3, Grey: 1
LOCA_STRIDE     = 8
LOCA_CLASSES    = {0: "crazyflie"}
TRAIN_ANNOT_PATH    = "./dataset/{}/train.txt".format(DATASET_FOLDER)
TRAIN_BATCH_SIZE    = 5
TRAIN_INPUT_SIZE    = [224, 320]
TRAIN_LR_INIT       = 1e-3
TRAIN_LR_END        = 1e-6
TRAIN_WARMUP_EPOCHS = 2
TRAIN_EPOCHS        = 15