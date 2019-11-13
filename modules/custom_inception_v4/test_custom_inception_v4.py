import tensorflow as tf
from PIL import Image
from config import *
import numpy as np

from tf_slim.research.slim.nets import inception_v4, inception_utils, inception
from tf_slim.research.slim.preprocessing.inception_preprocessing import preprocess_image
slim = tf.contrib.slim

IMAGE_SIZE = 299
IMAGE_PATH = '/home/tien/Works/DH/final/project/data/42/123798.jpg'

if __name__ == '__main__':
    with tf.Graph().as_default():

        image = Image.open(IMAGE_PATH)
        image = np.array(image)
        image = tf.compat.v1.convert_to_tensor(image)
        # image = tf.io.decode_image(image)
        processed_image = preprocess_image(image, IMAGE_SIZE, IMAGE_SIZE, is_training=False, crop_image=True)
        processed_images = tf.expand_dims(processed_image, 0)

        with slim.arg_scope(inception_v4.inception_v4_arg_scope()):
            logits, end_points = inception_v4.inception_v4(inputs=processed_images, num_classes=10001, is_training=False)

        probabilities = tf.nn.softmax(logits)

        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, os.path.join(MODEL_CHECKPOINT_PATH, INCEPTION_V4_CKPT_PATH))

            np_image, network_input, probabilities = sess.run([image, processed_images, probabilities])

        debug =1
