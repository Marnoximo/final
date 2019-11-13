from modules.common import xml_helper
import pandas as pd
import os
from tqdm import tqdm

test_groundtruth_file = '/home/tien/Works/DH/final/project/data/plc_vnc_test.csv'
test_image_folder = '/home/tien/Works/DH/final/data/data_tien/plc_test/plc_test'

xml_list = [fn for fn in os.listdir(test_image_folder) if fn.endswith(".xml")]
df = pd.read_csv(test_groundtruth_file)

for xml_file in tqdm(xml_list):
    media_id = xml_file.split(".")[0]
    class_id = df[df["MediaId"] == int(media_id)]["ClassId"].values.tolist()[0]

    abs_path = os.path.join(test_image_folder, xml_file)
    xml_data = xml_helper.read_xml(abs_path)
    xml_data = xml_helper.add_element_to_root(xml_data, "ClassId", str(class_id))
    xml_helper.write_xml(abs_path, xml_data)