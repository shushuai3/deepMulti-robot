import os
import cv2
import random
import numpy as np
import tensorflow as tf
import config as cfg

class Dataset(object):

    def __init__(self, dataset_type):
        self.annot_path  = cfg.TRAIN_ANNOT_PATH if dataset_type == 'train' else cfg_TEST.ANNOT_PATH
        self.input_size  = cfg.TRAIN_INPUT_SIZE if dataset_type == 'train' else cfg_TEST.INPUT_SIZE
        self.batch_size  = cfg.TRAIN_BATCH_SIZE if dataset_type == 'train' else cfg_TEST.BATCH_SIZE

        self.stride = cfg.LOCA_STRIDE
        self.classes = cfg.LOCA_CLASSES
        self.num_classes = len(self.classes)

        self.annotations = self.load_annotations()
        self.num_samples = len(self.annotations)
        self.num_batchs  = int(np.ceil(self.num_samples / self.batch_size))
        self.batch_count = 0
        self.input_channel = cfg.INPUT_CHANNEL

    def load_annotations(self):
        with open(self.annot_path, 'r') as f:
            txt = f.readlines()
            annotations = [line.strip() for line in txt if len(line.strip().split()[1:]) != 0]
        np.random.shuffle(annotations)
        return annotations

    def __iter__(self):
        return self

    def __next__(self):
        with tf.device('/cpu:0'):
            self.output_size = np.array(self.input_size) // self.stride
            batch_image = np.zeros((self.batch_size, self.input_size[0], self.input_size[1], self.input_channel), dtype=np.float32)
            batch_label = np.zeros((self.batch_size, self.output_size[0], self.output_size[1], 4 + self.num_classes), dtype=np.float32)

            num = 0
            if self.batch_count < self.num_batchs:
                while num < self.batch_size:
                    index = self.batch_count * self.batch_size + num
                    if index >= self.num_samples: index -= self.num_samples
                    annotation = self.annotations[index]
                    image, points = self.parse_annotation(annotation)
                    label_point = self.preprocess_true_points(points)

                    batch_image[num, :, :, :] = image
                    batch_label[num, :, :, :] = label_point
                    num += 1
                self.batch_count += 1
                return batch_image, batch_label
            else:
                self.batch_count = 0
                np.random.shuffle(self.annotations)
                raise StopIteration

    def parse_annotation(self, annotation):
        line = annotation.split()
        image_path = line[0]
        if not os.path.exists(image_path):
            raise KeyError("%s does not exist ... " %image_path)
        if cfg.DATASET_FOLDER == 'synImgs':
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = image[..., np.newaxis]
        image = np.swapaxes(np.copy(image),0,1)
        points = np.array([list(map(int, point.split(','))) for point in line[2:3]])
        return image, points

    def preprocess_true_points(self, points):
        label = np.zeros((self.output_size[0], self.output_size[1], 4+self.num_classes))
        for point in points:
            point_xy    = point[:2]
            point_depth = point[2]
            point_class = point[3]

            onehot = np.zeros(self.num_classes, dtype=np.float)
            onehot[point_class] = 1.0
            uniform_distribution = np.full(self.num_classes, 1.0 / self.num_classes)
            deta = 0.01
            smooth_onehot = onehot * (1 - deta) + deta * uniform_distribution

            xind, yind = point_xy // self.stride
            label[xind, yind, 0:2] = point_xy
            label[xind, yind, 2] = point_depth
            label[xind, yind, 3] = 1.0
            label[xind, yind, 4:] = smooth_onehot
        label_point = label
        return label_point

    def __len__(self):
        return self.num_batchs