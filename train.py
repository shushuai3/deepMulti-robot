import os
import shutil
import tensorflow as tf
from dataset import Dataset
from locaNet import locaNet, compute_loss
import config as cfg

logdir = "./output/log"
if os.path.exists(logdir): shutil.rmtree(logdir)
writer = tf.summary.create_file_writer(logdir)

trainset = Dataset('train')
steps_per_epoch = len(trainset)
global_steps = tf.Variable(1, trainable=False, dtype=tf.int64)
warmup_steps = cfg.TRAIN_WARMUP_EPOCHS * steps_per_epoch
total_steps = cfg.TRAIN_EPOCHS * steps_per_epoch

input_tensor = tf.keras.layers.Input([320, 224, cfg.INPUT_CHANNEL])
conv_tensors = locaNet(input_tensor) # 40x28x(2 + class)

model = tf.keras.Model(input_tensor, conv_tensors)
optimizer = tf.keras.optimizers.Adam()

def train_step(image_data, target):
    with tf.GradientTape() as tape:
        pred_result = model(image_data, training=True)
        loss_items = compute_loss(pred_result, target)
        depth_loss  = loss_items[0]
        conf_loss   = loss_items[1]
        prob_loss   = loss_items[2]
        total_loss = depth_loss + conf_loss + prob_loss

        gradients = tape.gradient(total_loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        tf.print("=> STEP %4d   lr: %.6f   depth_loss: %4.2f   conf_loss: %4.2f   "
                 "prob_loss: %4.2f   total_loss: %4.2f" %(global_steps, optimizer.lr.numpy(),
                                                          depth_loss, conf_loss,
                                                          prob_loss, total_loss))
        # update learning rate
        global_steps.assign_add(1)
        if global_steps < warmup_steps:
            lr = global_steps / warmup_steps *cfg.TRAIN_LR_INIT
        else:
            lr = cfg.TRAIN_LR_END + 0.5 * (cfg.TRAIN_LR_INIT - cfg.TRAIN_LR_END) * (
                (1 + tf.cos((global_steps - warmup_steps) / (total_steps - warmup_steps) * 3.1415))
            )
        optimizer.lr.assign(lr.numpy())

        # writing summary data
        with writer.as_default():
            tf.summary.scalar("lr", optimizer.lr, step=global_steps)
            tf.summary.scalar("loss/total_loss", total_loss, step=global_steps)
            tf.summary.scalar("loss/depth_loss", depth_loss, step=global_steps)
            tf.summary.scalar("loss/conf_loss", conf_loss, step=global_steps)
            tf.summary.scalar("loss/prob_loss", prob_loss, step=global_steps)
        writer.flush()

for epoch in range(cfg.TRAIN_EPOCHS):
    for image_data, target in trainset:
        train_step(image_data, target)
    model.save_weights("./output/locaNet")
    model.save("./output/model.h5")