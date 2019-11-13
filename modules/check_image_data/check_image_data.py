import os
from config import *
import pandas as pd
from tqdm import tqdm

def image_number_report():
    class_dirs = [fn for fn in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, fn))]

    entries = []
    for cls_dir in tqdm(class_dirs):
        image_path = os.path.join(DATA_PATH, cls_dir)
        image_fns = [fn for fn in os.listdir(image_path) if not fn.startswith('.')]
        entries.append({'class_id': cls_dir, 'num_images': len(image_fns)})

    return pd.DataFrame(entries)


if __name__ == '__main__':
    report_df = image_number_report()
    report_df.to_csv(os.path.join(REPORT_PATH, 'image_number_report.csv'))
    print(report_df.info())