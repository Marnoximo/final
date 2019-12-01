import pandas as pd
import argparse
import os
import logging

from modules.common.db.database import DBHelper, ModelLabel
from config import DevelopmentConfig

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--label_file', type=str, required=True)
parser.add_argument('--species_file', type=str, required=True)
parser.add_argument('--model_name', type=str, required=True)
args = parser.parse_args()

label_file = args.label_file
if not os.path.isfile(label_file):
    logger.error('Label file not exist')

species_file = args.species_file
if not os.path.isfile(species_file):
    logger.error('Species file not exist')

model_name = args.model_name

with open(label_file) as file:
    lines = file.readlines()
    label_list = [{'label': line.split(':')[0], 'ClassId': line.split(':')[1].strip('\n')} for line in lines]
    label_df = pd.DataFrame(label_list, dtype=str)

species_df = pd.read_csv(args.species_file, dtype=str)
species_df['vnc_id'] = species_df['vnc_url'].apply(lambda x: x.split('ID=')[-1])

join_df = species_df.merge(
    label_df, how='inner', left_on='ClassId', right_on='ClassId'
)

DBHelper.connect_database(DevelopmentConfig())
for index, row in join_df.iterrows():
    vnc_id = row['vnc_id']
    label = row['label']
    # d =1
    ModelLabel.create(DBHelper.get_session(), **{
        'vnc_id': str(vnc_id),
        'label_id': int(label),
        'model_name': model_name
    })
