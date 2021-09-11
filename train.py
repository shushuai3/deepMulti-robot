import os
import shutil
import tensorflow as tf
from dataset import Dataset
from locaNet import locaNet, compute_loss
import config as cfg

logdir = "./output/log"
if os.path.exists(logdir): shutil.rmtree(logdir)
writer = tf.summary.create_file_writer(logdir)

trainset = Dataset()
steps_per_epoch = len(trainset)
global_steps = tf.Variable(1, trainable=False, dtype=tf.int64)
warmup_steps = cfg.TRAIN_WARMUP_EPOCHS * steps_per_epoch
total_steps = cfg.TRAIN_EPOCHS * steps_per_epoch

input_tensor = tf.keras.layers.Input([224, 320, cfg.INPUT_CHANNEL])
conv_tensors = locaNet(input_tensor)

model = tf.keras.Model(input_tensor, conv_tensors)
optimizer = tf.keras.optimizers.Adam()

def train_step(image_data, target):
    with tf.GradientTape() as tape:
        # Prediction, loss and gradient. Output 28x40x2 (depth and confidence)
        pred_result = model(image_data, training=True)
        loss_items = compute_loss(pred_result, target)
        depth_loss  = loss_items[0]
        conf_loss   = loss_items[1]
        total_loss = depth_loss + conf_loss

        gradients = tape.gradient(total_loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        tf.print("STEP %4d   lr: %.6f   depth_loss: %4.2f   conf_loss: %4.2f   "
                 "total_loss: %4.2f" %(global_steps, optimizer.lr.numpy(),
                 depth_loss, conf_loss, total_loss))

        # Change learning rate
        global_steps.assign_add(1)
        if global_steps < warmup_steps:
            lr = global_steps / warmup_steps *cfg.TRAIN_LR_INIT
        else:
            lr = cfg.TRAIN_LR_END + 0.5 * (cfg.TRAIN_LR_INIT - cfg.TRAIN_LR_END) * (
                (1 + tf.cos((global_steps - warmup_steps) / (total_steps - warmup_steps) * 3.1415))
            )
        optimizer.lr.assign(lr.numpy())

        # Write summary data
        with writer.as_default():
            tf.summary.scalar("lr", optimizer.lr, step=global_steps)
            tf.summary.scalar("loss/total_loss", total_loss, step=global_steps)
            tf.summary.scalar("loss/depth_loss", depth_loss, step=global_steps)
            tf.summary.scalar("loss/conf_loss", conf_loss, step=global_steps)
        writer.flush()

for epoch in range(cfg.TRAIN_EPOCHS):
    for image_data, target in trainset:
        train_step(image_data, target)
    model.save_weights("./output/locaNet")
    model.save("./output/loca.h5")