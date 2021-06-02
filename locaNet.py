import numpy as np
import tensorflow as tf
import common as common
import config as cfg
NUM_CLASS = len(cfg.LOCA_CLASSES)

def locaNet(input_layer):
    input_data = common.convolutional(input_layer, (3, 3, cfg.INPUT_CHANNEL, 8)) # 320x224x8
    input_data = common.convolutional(input_data, (3, 3, 8, 16), downsample=True) # 160x112x16
    input_data = common.convolutional(input_data, (3, 3, 16, 32), downsample=True) # 80x56x32
    input_data = common.convolutional(input_data, (3, 3, 32, 64), downsample=True) # 40x28x64
    route_1 = input_data
    input_data = common.convolutional(input_data, (3, 3, 64, 128), downsample=True) # 20x14x128
    route_2 = input_data
    input_data = common.convolutional(input_data, (3, 3, 128, 256), downsample=True) # 10x7x256
    conv = common.convolutional(input_data, (1, 1, 256, 128)) # 10x7x128
    conv = common.upsample(conv) # 20x14x128
    conv = tf.keras.layers.Concatenate(axis=-1)([conv, route_2]) # 20x14x256
    conv = common.convolutional(conv, (1, 1, 256, 128)) # 20x14x128
    conv = common.upsample(conv) # 40x28x128
    conv = tf.keras.layers.Concatenate(axis=-1)([conv, route_1]) # 40x28x192
    conv_point = common.convolutional(input_data, (1, 1, 192, 2+NUM_CLASS), activate=False, bn=False) # 40x28x(2 + NUM_CLASS)
    return conv_point

def compute_loss(conv, label):
    conv_shape  = tf.shape(conv)
    batch_size  = conv_shape[0]
    output_size = conv_shape[1:3]
    conv = tf.reshape(conv, (batch_size, output_size[0], output_size[1], 2 + NUM_CLASS))

    conv_raw_conf = conv[:, :, :, 1:2]
    conv_raw_prob = conv[:, :, :, 2:]

    pred_d      = tf.exp(conv[:, :, :, 0:1])
    pred_conf   = tf.sigmoid(conv[:, :, :, 1:2])

    label_d     = label[:, :, :, 2:3]
    label_conf  = label[:, :, :, 3:4]
    label_prob  = label[:, :, :, 4:]

    conf_focal  = tf.pow(label_conf - pred_conf, 2)
    conf_loss   = conf_focal * (tf.nn.sigmoid_cross_entropy_with_logits(labels=label_conf, logits=conv_raw_conf))
    prob_loss   = label_conf * tf.nn.sigmoid_cross_entropy_with_logits(labels=label_prob, logits=conv_raw_prob)
    depth_loss  = label_conf * tf.pow(pred_d - label_d/1000.0, 2)

    depth_loss  = tf.reduce_mean(tf.reduce_sum(depth_loss, axis=[1,2,3]))
    conf_loss   = tf.reduce_mean(tf.reduce_sum(conf_loss, axis=[1,2,3]))
    prob_loss   = tf.reduce_mean(tf.reduce_sum(prob_loss, axis=[1,2,3]))
    return depth_loss, conf_loss, prob_loss