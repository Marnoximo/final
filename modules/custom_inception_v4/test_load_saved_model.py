from config import *

from PIL import Image
import numpy as np

import tensorflow as tf
slim = tf.contrib.slim

from tf_slim.research.slim.preprocessing.inception_preprocessing import *
from tf_slim.research.slim.datasets import flowers

flowers.get_split('train', '')
with tf.Graph().as_default():
    image = Image.open(os.path.join(DATA_PATH, '42/123798.jpg'))

    image = np.array(image)
    # image = tf.compat.v1.convert_to_tensor(image)
    #
    # proc_image = preprocess_image(image, 299, 299, is_training=False, crop_image=True)
    # proc_image = tf.expand_dims(proc_image, 0)
    with tf.Session() as sess:
        tf.saved_model.loader.load(sess, ["serve"], SAVED_MODEL_PATH + '/201019_1')
        graph = tf.get_default_graph()
        tensors = graph.as_graph_def().node
        for ts in tensors:
            print(ts.name)
        input_image = graph.get_tensor_by_name('my_input:0')
        pred = sess.run("InceptionV4/Logits/Predictions:0", feed_dict={input_image: image})
        print(pred)

