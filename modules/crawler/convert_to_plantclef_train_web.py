import pandas as pd
import os
import json
from config import *

template_path = 'data/train_web_template.csv'
tmp_df = pd.read_csv(os.path.join(PROJECT_PATH, template_path))
tmp_df['ObservationId'] = 0


def make_entry(class_id, url, origin, media_id):
    entry = tmp_df[tmp_df['ClassId'] == class_id].iloc[0, 1:]
    entry['OriginalUrl'] = url
    entry['BackUpLink'] = url
    entry['Origin'] = origin
    # media_id = url.split('/')[-1].split('.')[0].replace('_', '')
    # entry['MediaId'] = 3000000 + int(media_id)
    entry['MediaId'] = media_id
    return entry


def convert_to_plantclef(df, origin):
    output = []

    for idx, row in df.iterrows():
        class_id = row['ClassId']
        url = row['image_url']

        entry = make_entry(class_id, url, origin, idx)
        output.append(entry)

    return pd.DataFrame(output)

