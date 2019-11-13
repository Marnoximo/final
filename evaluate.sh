#!/usr/bin/env bash

DATASET_DIR="/home/tien/Works/DH/final/data/data_tien/plc_test/"
CHECKPOINT_PATH="/home/tien/Works/DH/final/project/models/plc_vnc/model.ckpt-565"

python modules/eval_image_classifier.py \
    --alsologtostderr \
    --checkpoint_path=${CHECKPOINT_PATH} \
    --dataset_dir=${DATASET_DIR} \
    --dataset_name=plc_test \
    --dataset_split_name=test \
    --model_name=inception_v4