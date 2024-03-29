# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Downloads and converts a particular dataset.

Usage:
```shell

$ python download_and_convert_data.py \
    --dataset_name=mnist \
    --dataset_dir=/tmp/mnist

$ python download_and_convert_data.py \
    --dataset_name=cifar10 \
    --dataset_dir=/tmp/cifar10

$ python download_and_convert_data.py \
    --dataset_name=flowers \
    --dataset_dir=/tmp/flowers

  python3 download_and_convert_data.py   --dataset_name=flowers  --dataset_dir=flowers

  download_and_convert_data.py     --dataset_name=plantclef    --dataset=training_data_2015     --dataset_dir=plantclef2015

  download_and_convert_data.py     --dataset_name=plantclef    --dataset=test_data_2015     --dataset_dir=plantclef2015_test

  download_and_convert_data.py     --dataset_name=plantclef    --dataset=whole_data_2015_whole     --dataset_dir=plantclef2015_whole

  download_and_convert_data.py     --dataset_name=plantclef    --dataset=test_data_2016     --dataset_dir=plantclef2016_test

  python3 download_and_convert_data.py \
    --dataset_name=plantVSnoplant \
    --dataset_dir= plantVSnoplant

```
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from modules.datasets import download_and_convert_tien
from modules.datasets import download_and_convert_tien_for_test

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
    'dataset_name',
    None,
    'The name of the dataset to convert, one of "training_data_2017", "test_data_2017", "vnc_data", "google_data"')

tf.app.flags.DEFINE_string(
    'dataset',
    None,
    'The name of the plantclef data to convert, one of "training_data_2014", "training_data_2015", "test_data_2015", "whole_data_2015"')

tf.app.flags.DEFINE_string(
    'dataset_dir',
    None,
    'The directory where the output TFRecords and temporary files are saved.')

tf.app.flags.DEFINE_string(
    'validation_rate',
    '0.2',
    'The rate of validation set/whole set'
)


def main(_):
    if not FLAGS.dataset_name:
        raise ValueError('You must supply the dataset name with --dataset_name')
    if not FLAGS.dataset_dir:
        raise ValueError('You must supply the dataset directory with --dataset_dir')

    if FLAGS.dataset_name == 'data_tien':
        if FLAGS.dataset in ['plc_vnc_web', 'plc_vnc']:
            download_and_convert_tien.run(FLAGS.dataset_dir, FLAGS.dataset, float(FLAGS.validation_rate))
        elif FLAGS.dataset == 'plc_test':
            download_and_convert_tien_for_test.run(FLAGS.dataset_dir, FLAGS.dataset)
        else:
            raise ValueError(
                'dataset [%s] was not recognized.' % FLAGS.dataset)
    else:
        raise ValueError(
            'dataset_name [%s] was not recognized.' % FLAGS.dataset_dir)


if __name__ == '__main__':
    tf.app.run(
        # argv={'dataset_name': 'plantclef', 'dataset': 'vncreature', 'dataset_dir': '/home/tien/Works/DH/final/data/data_tien/vncreature'}
    )
