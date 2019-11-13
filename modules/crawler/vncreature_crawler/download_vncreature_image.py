import csv
import sys, os
from io import StringIO
from urllib.request import urlopen, URLError
from http import client
import ssl
import socket
from socket import error as SocketError
import errno
import threading

## Tien's mod
import pandas as pd

plc_vnc_csv = '/home/tien/Works/DH/final/project/reports/plantclef_vncreature_join_list.csv'
df = pd.read_csv(plc_vnc_csv)
class_list = df['ClassId'].values.tolist()
##

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

MAX_THREADS = 6
threadLimiter = threading.BoundedSemaphore(MAX_THREADS)

id_to_field = {}
id_to_field[0] = "Species"
id_to_field[1] = "Origin"
id_to_field[2] = "OriginalUrl"
id_to_field[3] = "Genus"
id_to_field[4] = "Family"
id_to_field[5] = "ObservationId"
id_to_field[6] = "MediaId"
id_to_field[7] = "YearInCLEF"
id_to_field[8] = "LearnTag"
id_to_field[9] = "ClassId"
id_to_field[10] = "BackUpLink"

field_to_id = {}
for c in id_to_field:
    f = id_to_field[c]
    field_to_id[f] = c

missed = []


def convert_to_xml_lines(row):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<Image>')
    filename = row[field_to_id['MediaId']] + '.jpg'
    lines.append('\t<FileName>' + filename + '</FileName>')
    for i in range(0, len(id_to_field)):
        s = id_to_field[i]
        lines.append('\t<' + s + '>' + row[i] + '</' + s + '>')
    lines.append('</Image>')
    return lines


class Thread(threading.Thread):

    def run(self, row, dir_out, timeout, missed):
        threadLimiter.acquire()
        try:
            self.process(row, dir_out, timeout, missed)
        finally:
            threadLimiter.release()

    def process(self, row, dir_out, timeout, missed):

        url = row[field_to_id['OriginalUrl']]
        # url = row[field_to_id['BackUpLink']]

        try:
            # data = urllib2.urlopen(url, timeout=timeout, context=ctx).read()
            data = urlopen(url, timeout=timeout, context=ctx).read()
            dir_out_sub = dir_out + '/' + row[field_to_id['ClassId']] + '/'
            if not os.path.isdir(dir_out_sub):
                os.makedirs(dir_out_sub)

            file_out_jpg = dir_out_sub + '/' + row[field_to_id['MediaId']] + '.jpg'
            jpg_file = open(file_out_jpg, 'wb')
            jpg_file.write(data)
            jpg_file.close()

            lines = convert_to_xml_lines(row)
            file_out_xml = dir_out_sub + '/' + row[field_to_id['MediaId']] + '.xml'
            xml_file = open(file_out_xml, 'w')
            for line in lines:
                xml_file.write(line + '\n')
            xml_file.close()

            print(url, ' -> ', file_out_jpg, ', ', file_out_xml)

        except URLError as e:
            print('  -> urlerror ', e, ', ', url)
        except ssl.SSLError:
            print('  -> ssl error ', url)
        except socket.timeout:
            print('  -> timeout ', url)
        except client.BadStatusLine:
            print('  -> badstatus ', url)
        except client.HTTPException:
            print('  -> httplib more than 100 headers ', url)
        except client.IncompleteRead:
            print('  -> httplib IncompleteRead ', url)
        except SocketError as es:
            if es.errno != errno.ECONNRESET:
                raise
            pass


def run(web_file, dir_out, timeout):
    print('load ', web_file)
    with open(web_file, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            break  # header
        for row in rows:
            thread = Thread()
            thread.run(row, dir_out, timeout, missed)


# by default
web_file = '/home/tien/Works/DH/final/project/modules/crawler/vncreature_crawler/vncreature_image_list.csv'
dir_out = '/home/tien/Works/DH/final/project/data/vncreature/'
timeout = 20

if len(sys.argv) == 4:
    web_file = sys.argv[1]
    dir_out = sys.argv[2]
    timeout = float(sys.argv[3])

# python download_lifeclef17_web_train_data.py PlantCLEF2017TrainWeb.csv data 20

run(web_file, dir_out, timeout)
