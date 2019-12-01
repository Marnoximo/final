# Common variables
DATA_PATH = '/home/tien/Works/DH/final/data/PlantCLEF2017Train1EOL/data/'
MODEL_CHECKPOINT_PATH = '/home/tien/Works/DH/final/models/lifeclef2018/'
REPORT_PATH = '/home/tien/Works/DH/final/project/reports/'
TF_SLIM_PATH = '/home/tien/Works/DH/final/project/tf_slim/research/slim'
SAVED_MODEL_PATH = '/home/tien/Works/DH/final/project/saved_models/'
PROJECT_PATH = '/home/tien/Works/DH/final/project/'

INCEPTION_V4_CKPT_PATH = 'inception_v4/model.ckpt-2060000'

# Add TF Slim repo to system path
import sys
sys.path.append("/home/tien/Works/DH/final/project/tf_slim/research/slim")

# Config GPU for Tensorflow
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '1'


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    sys.path.append("/home/tien/Works/DH/final/project/tf_slim/research/slim")
    os.environ["CUDA_VISIBLE_DEVICES"] = '1'


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    ENV = 'development'
    TESTING = True

    DATABASE_URI = 'mysql+pymysql://admin:tienfinal@127.0.0.1/plantqt?charset=utf8mb4'


class ProductionConfig(BaseConfig):
    DEBUG = True
    ENV = 'production'
    TESTING = True

    DATABASE_URI = ''