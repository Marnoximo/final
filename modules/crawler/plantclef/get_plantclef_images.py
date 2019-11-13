import os
import pandas as pd
from shutil import copy

plantclef_train_path = '/home/tien/Works/DH/final/data/PlantCLEF2017Train1EOL/data'
plantclef_test_path = '/home/tien/Works/DH/final/data/PlantCLEF2017Test/data'
plc_vnc_class_path = '/home/tien/Works/DH/final/project/reports/plantclef_vncreature_join_list.csv'
plc_vnc_test_path = '/home/tien/Works/DH/final/project/data/plc_vnc_test.csv'
output_train_path = '/home/tien/Works/DH/final/data/data_tien/plantclef2017_train'
output_test_path = '/home/tien/Works/DH/final/data/data_tien/plantclef2017_test'

if not os.path.exists(output_train_path):
    os.mkdir(output_train_path)

if not os.path.exists(output_test_path):
    os.mkdir(output_test_path)


def copy_train():
    df = pd.read_csv(plc_vnc_class_path)

    for idx, row in df.iterrows():
        class_id = row['ClassId']

        # Copy train images
        class_dir = os.path.join(plantclef_train_path, str(class_id))
        if not os.path.exists(class_dir):
            print('Copy train images for class {} failed. Folder not exist'.format(class_id))
        else:
            output_class_dir = os.path.join(output_train_path, str(class_id))
            if not os.path.exists(output_class_dir):
                os.mkdir(output_class_dir)

            for fn in os.listdir(class_dir):
                if fn.startswith('.'):
                    continue

                src = os.path.join(class_dir, fn)
                dst = os.path.join(output_class_dir, fn)
                print(src, ' => ', dst)
                copy(src, dst)

            print('\n[INFO] Copied all images for class={}\n'.format(class_id))


def copy_test():
    df = pd.read_csv(plc_vnc_test_path)
    for idx, row in df.iterrows():
        media_id = row['MediaId']

        jpg_file = os.path.join(plantclef_test_path, str(media_id)+'.jpg')
        if not os.path.exists(jpg_file):
            print('Image file with mediaid={} does not exist'.format(media_id))
            continue
        dst = os.path.join(output_test_path, str(media_id)+'.jpg')
        print(jpg_file, " => ", dst)
        copy(jpg_file, dst)

        xml_file = os.path.join(plantclef_test_path, str(media_id)+'.xml')
        if not os.path.exists(xml_file):
            print('Xml file with mediaid={} does not exist'.format(media_id))
            continue
        dst = os.path.join(output_test_path, str(media_id) + '.xml')
        print(xml_file, " => ", dst)
        copy(xml_file, dst)


if __name__ == '__main__':
    print("Copy train images")
    copy_train()

    print("Copy test images")
    copy_test()