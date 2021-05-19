import tensorflow as tf

class BatchNormalization(tf.keras.layers.BatchNormalization):
    def call(self, x, training=tf.constant(False)):
        training = tf.logical_and(training, self.trainable)
        return super().call(x, training)

def convolutional(input_layer, filters_shape, downsample=False, activate=True, bn=True):
    if downsample:
        input_layer = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid')(input_layer)
    strides = 1
    padding = 'same'
    conv = tf.keras.layers.Conv2D(filters=filters_shape[-1], kernel_size = filters_shape[0], strides=strides, padding=padding,
                        use_bias=not bn, kernel_regularizer=tf.keras.regularizers.l2(0.0005),
                        kernel_initializer=tf.random_normal_initializer(stddev=0.01),
                        bias_initializer=tf.constant_initializer(0.))(input_layer)
    if bn: conv = BatchNormalization()(conv)
    if activate == True:
        conv = tf.keras.layers.Activation('relu')(conv)
    return conv

def residual_block(input_layer, input_channel, filter_num1, filter_num2):
    short_cut = input_layer
    conv = convolutional(input_layer, filters_shape=(1, 1, input_channel, filter_num1))
    conv = convolutional(conv       , filters_shape=(3, 3, filter_num1,   filter_num2))
    residual_output = tf.keras.layers.Add()([short_cut, conv])
    return residual_output

def upsample(input_layer):
    return tf.keras.layers.UpSampling2D(size=(2, 2))(input_layer)