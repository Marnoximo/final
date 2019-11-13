from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import tensorflow as tf

from modules.datasets import dataset_utils

slim = tf.contrib.slim

_FILE_PATTERN_Training = '{dataset_name}_{data_split_name}_*.tfrecord'
_DATASETS = ['plc_vnc_web', 'plc_vnc', 'plc_test']
_SPLITS = ['train', 'validation', 'test']

_ITEMS_TO_DESCRIPTIONS = {
    'image': 'A color image of varying size.',
    'label_species': 'A single integer between 0 and 999 ',
    'label_genus': 'A single integer between 0 and 515',
    'label_family': 'A single integer between 0 and 123',
    'label_organ': 'A single integer between 0 and 6'
}


def get_split(dataset, split_name, dataset_dir, file_pattern=None, reader=None):
    """Gets a dataset tuple with instructions for reading flowers.

    Args:
      split_name: A train/validation split name.
      dataset_dir: The base directory of the dataset sources.
      file_pattern: The file pattern to use when matching the dataset sources.
        It is assumed that the pattern contains a '%s' string so that the split
        name can be inserted.
      reader: The TensorFlow reader type.

    Returns:
      A `Dataset` namedtuple.

    Raises:
      ValueError: if `split_name` is not a valid train/validation split.
    """
    if dataset not in _DATASETS:
        raise ValueError('Dataset %s was not recognized.' % dataset)
    if split_name not in _SPLITS:
        raise ValueError('split name %s was not recognized.' % split_name)

    if not file_pattern:
        file_pattern = _FILE_PATTERN_Training
    file_pattern = os.path.join(dataset_dir, file_pattern.format(dataset_name=dataset, data_split_name=split_name))

    # Allowing None in the signature so that dataset_factory can use the default.
    if reader is None:
        reader = tf.TFRecordReader

    js = json.load(open(os.path.join(dataset_dir, 'dataset_info.json')))
    num_classes = js['num_classes']

    if split_name != 'test':
        keys_to_features = {'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
                            'image/format': tf.FixedLenFeature((), tf.string, default_value='png'),
                            'image/class/label_species': tf.FixedLenFeature([], tf.int64,
                                                                            default_value=tf.zeros([], dtype=tf.int64)),
                            'image/class/label_genus': tf.FixedLenFeature([], tf.int64,
                                                                          default_value=tf.zeros([], dtype=tf.int64)),
                            'image/class/label_family': tf.FixedLenFeature([], tf.int64,
                                                                           default_value=tf.zeros([], dtype=tf.int64)),
                            'image/class/label_organ': tf.FixedLenFeature([], tf.int64,
                                                                          default_value=tf.zeros([], dtype=tf.int64))}

        items_to_handlers = {'image': slim.tfexample_decoder.Image(),
                             'label_species': slim.tfexample_decoder.Tensor('image/class/label_species'),
                             'label_genus': slim.tfexample_decoder.Tensor('image/class/label_genus'),
                             'label_family': slim.tfexample_decoder.Tensor('image/class/label_family'),
                             'label_organ': slim.tfexample_decoder.Tensor('image/class/label_organ')}
        if split_name == 'train':
            num_samples = js['training_size']
        elif split_name == 'validation':
            num_samples = js['validation_size']

    else:
        keys_to_features = {'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
                            'image/format': tf.FixedLenFeature((), tf.string, default_value='png'),
                            'image/media_id': tf.FixedLenFeature([], tf.int64,
                                                                    default_value=tf.zeros([], dtype=tf.int64)),
                            'image/class_id': tf.FixedLenFeature([], tf.int64,
                                                                    default_value=tf.zeros([], dtype=tf.int64))}

        items_to_handlers = {'image': slim.tfexample_decoder.Image(),
                             'image_id': slim.tfexample_decoder.Tensor('image/media_id'),
                             'class_id': slim.tfexample_decoder.Tensor('image/class_id')}

        num_samples = js['test_size']


    decoder = slim.tfexample_decoder.TFExampleDecoder(keys_to_features, items_to_handlers)

    labels_to_names = None
    if dataset_utils.has_labels(dataset_dir):
        labels_to_names = dataset_utils.read_label_file(dataset_dir)

    return slim.dataset.Dataset(
        data_sources=file_pattern,
        reader=reader,
        decoder=decoder,
        num_samples=num_samples,
        items_to_descriptions=_ITEMS_TO_DESCRIPTIONS,
        num_classes=num_classes,
        labels_to_names=labels_to_names)


if __name__ == '__main__':
    dataset = get_split('plc_test', 'test', '/home/tien/Works/DH/final/data/data_tien/plc_test')
    debug = 1