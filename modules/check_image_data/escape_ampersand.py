from PIL import Image
import os

path = '/home/tien/Works/DH/final/data/data_tien/plantclef_train/PlantCLEF2017Train1EOL'

for dir in os.listdir(path):
    for fn in os.listdir(os.path.join(path, dir)):
        if fn.endswith('.xml'):
            data = []
            fp = os.path.join(path, dir, fn)
            for line in open(fp, 'r').readlines():
                line = line.replace('&', '&amp;')
                data.append(line)

            with open(fp, 'w') as f:
                f.writelines(data)


# for fn in errors:
#     os.remove(fn)
#     os.remove(fn.replace('jpg', 'xml'))