import tensorflow as tf
import common as common
import config as cfg

def locaNet(input_layer):
    input_data = common.convolutional(input_layer, (3, 3, cfg.INPUT_CHANNEL, 8))    # 224x320x8
    input_data = common.convolutional(input_data, (3, 3, 8, 16), downsample=True)   # 112x160x16
    input_data = common.convolutional(input_data, (3, 3, 16, 32), downsample=True)  # 56x80x32
    input_data = common.convolutional(input_data, (3, 3, 32, 64), downsample=True)  # 28x40x64
    conv_point = common.convolutional(input_data, (1, 1, 64, 2+len(cfg.LOCA_CLASSES)), activate=False, bn=False)  # 28x40x(2+NumClass)
    # route_1 = input_data
    # input_data = common.convolutional(input_data, (3, 3, 64, 128), downsample=True) # 14x20x128
    # route_2 = input_data
    # input_data = common.convolutional(input_data, (3, 3, 128, 256), downsample=True) # 7x10x256
    # conv = common.convolutional(input_data, (1, 1, 256, 128)) # 7x10x128
    # conv = common.upsample(conv) # 14x20x128
    # conv = tf.keras.layers.Concatenate(axis=-1)([conv, route_2]) # 14x20x256
    # conv = common.convolutional(conv, (1, 1, 256, 128)) # 14x20x128
    # conv = common.upsample(conv) # 28x40x128
    # conv = tf.keras.layers.Concatenate(axis=-1)([conv, route_1]) # 28x40x192
    # conv_point = common.convolutional(conv, (1, 1, 192, 2+len(cfg.LOCA_CLASSES)), activate=False, bn=False) # 28x40x(2+NumClass)
    return conv_point

def compute_loss(conv, label):
    conv_shape  = tf.shape(conv)
    batch_size  = conv_shape[0]
    output_size = conv_shape[1:3]
    conv = tf.reshape(conv, (batch_size, output_size[0], output_size[1], 2+len(cfg.LOCA_CLASSES)))

    conv_raw_conf = conv[:, :, :, 1:2]
    conv_raw_prob = conv[:, :, :, 2:]

    pred_depth  = tf.exp(conv[:, :, :, 0:1])
    pred_conf   = tf.sigmoid(conv[:, :, :, 1:2])

    label_depth = label[:, :, :, 2:3]
    label_conf  = label[:, :, :, 3:4]
    label_prob  = label[:, :, :, 4:]

    conf_focal  = tf.pow(label_conf - pred_conf, 2)
    conf_loss   = conf_focal * (tf.nn.sigmoid_cross_entropy_with_logits(labels=label_conf, logits=conv_raw_conf))
    prob_loss   = label_conf * tf.nn.sigmoid_cross_entropy_with_logits(labels=label_prob, logits=conv_raw_prob)
    depth_loss  = label_conf * tf.pow(pred_depth - label_depth/1000.0, 2)

    depth_loss  = tf.reduce_mean(tf.reduce_sum(depth_loss, axis=[1,2,3]))
    conf_loss   = tf.reduce_mean(tf.reduce_sum(conf_loss, axis=[1,2,3]))
    prob_loss   = tf.reduce_mean(tf.reduce_sum(prob_loss, axis=[1,2,3]))
    return depth_loss, conf_loss, prob_loss