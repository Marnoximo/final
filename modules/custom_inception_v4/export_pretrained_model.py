import tensorflow as tf
from config import *
from tf_slim.research.slim.nets import inception_v4, inception, inception_utils
from tf_slim.research.slim.preprocessing.inception_preprocessing import *
slim = tf.contrib.slim

IMAGE_SIZE = 299

with tf.Graph().as_default():
    image = tf.placeholder(tf.float32, [None, None, 3], name='my_input')
    image = tf.compat.v1.convert_to_tensor(image)
    # image = tf.io.decode_image(image)
    processed_image = preprocess_image(image, IMAGE_SIZE, IMAGE_SIZE, is_training=False, crop_image=True)
    processed_images = tf.expand_dims(processed_image, 0)

    with tf.Session() as sess:

        with slim.arg_scope(inception_v4.inception_v4_arg_scope()):
            logits, end_points = inception_v4.inception_v4(processed_images, num_classes=10001, is_training=False)
        graph = tf.get_default_graph()
        ops = graph.get_operations()
        name_scope = graph.get_name_scope()
        tf.train.Saver().restore(sess, os.path.join(MODEL_CHECKPOINT_PATH, INCEPTION_V4_CKPT_PATH))

        tf.saved_model.simple_save(sess, SAVED_MODEL_PATH + '/201019_1/', inputs={'my_input': image}, outputs={'my_output': graph.get_tensor_by_name('InceptionV4/Logits/Predictions:0')})