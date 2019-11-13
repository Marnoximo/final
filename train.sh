#!/usr/bin/env bash

TRAIN_DIR="models/plc_vnc/"
DATASET_DIR="/home/tien/Works/DH/final/data/data_tien/plc_vnc/"
CHECKPOINT_PATH="/home/tien/Works/DH/final/models/lifeclef2018/inception_v4/model.ckpt-2060000"

python modules/train_image_classifier_plantclef.py \
    --train_dir=${TRAIN_DIR} \
    --dataset_dir=${DATASET_DIR} \
    --dataset_split_name=train \
    --dataset_name=plc_vnc \
    --model_name=inception_v4 \
    --checkpoint_path=${CHECKPOINT_PATH} \
    --checkpoint_exclude_scopes=InceptionV4/Logits,InceptionV4/AuxLogits \
    --trainable_scopes=InceptionV4/Logits,InceptionV4/AuxLogits