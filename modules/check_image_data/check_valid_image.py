from PIL import Image
import os

path = '/home/tien/Works/DH/final/data/data_tien/google/google'
err_image = '/home/tien/Works/DH/final/data/google/421/7606.jpg'

errors = []
cnt = 0
# for dir in os.listdir(path):
#     for fn in os.listdir(os.path.join(path, dir)):
#         if fn.endswith('.jpg'):
#             print(cnt)
#             cnt += 1
#             filepath = os.path.join(path, dir, fn)
#             try:
#                 # data = Image.open(filepath).convert('RGB')
#                 pass
#             except IOError as ex:
#                 print('Error')
#                 errors.append(filepath)
#                 continue
#
#             # data.save(filepath, 'JPEG')
#             # data.show()

for dir in os.listdir(path):
    for fn in os.listdir(os.path.join(path, dir)):
        if fn.endswith('.jpg'):
            xml_file = fn.replace('.jpg', '.xml')
            if not os.path.exists(os.path.join(path, dir, xml_file)):
                print('Error: ', fn)
                os.remove(os.path.join(path, dir, fn))

for dir in os.listdir(path):
    for fn in os.listdir(os.path.join(path, dir)):
        if fn.endswith('.xml'):
            xml_file = fn.replace('.xml', '.jpg')
            if not os.path.exists(os.path.join(path, dir, xml_file)):
                print('Error: ', fn)
                os.remove(os.path.join(path, dir, fn))
# for fn in errors:
#     os.remove(fn)
#     os.remove(fn.replace('jpg', 'xml'))