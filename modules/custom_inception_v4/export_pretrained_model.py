import tensorflow as tf
from config import *
from tf_slim.research.slim.nets import inception_v4, inception, inception_utils
from tf_slim.research.slim.preprocessing.inception_preprocessing import *
slim = tf.contrib.slim

IMAGE_SIZE = 299

with tf.Graph().as_default():
    image_bytes = tf.placeholder(tf.string, None, name='my_input')
    # image = tf.compat.v1.convert_to_tensor(image)
    image = tf.io.decode_jpeg(image_bytes, channels=3)
    processed_image = preprocess_image(image, IMAGE_SIZE, IMAGE_SIZE)
    processed_images = tf.expand_dims(processed_image, 0)

    with tf.Session() as sess:

        with slim.arg_scope(inception_v4.inception_v4_arg_scope()):
            logits, end_points = inception_v4.inception_v4(processed_images, num_classes=109, is_training=False)
        graph = tf.get_default_graph()
        ops = graph.get_operations()
        name_scope = graph.get_name_scope()
        tf.train.Saver().restore(sess, '/home/tien/Works/DH/final/project/models/plc_vnc/model.ckpt-565')

        tf.saved_model.simple_save(sess, SAVED_MODEL_PATH + '/1119_1/', inputs={'my_input': image_bytes}, outputs={'my_output': graph.get_tensor_by_name('InceptionV4/Logits/Predictions:0')})