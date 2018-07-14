
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

import pymongo
import redis

# 项目文件目录，基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置静态文件目录
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# mongodb 设置
MONGO = {
    "HOST": '127.0.0.1',
    "PORT": 27017,
    "DB": "renrenche",  # 数据库名称
    "COLLECTION": "",  # collection 的名称
    "USER": None,  # 用户名
    "PASSWORD": None,  # 密码
}

# redis 初始化配置
REDIS = {
    "HOST": '127.0.0.1',  # ip
    'PORT': 6379,  # 端口
    'USER': '',  # 用户
    'PASSWORD': '',  # 密码
}

# MySQL数据库配置
MYSQL = {
    "HOST": 'localhost',
    "PORT": 3306,
    "DB": 'rrc',  # 数据库名称
    "USER": 'root',  # 用户名
    "PASSWORD": '123456',  # 用户密码
}

# mongodb  连接
CONN = pymongo.MongoClient(
    host=MONGO["HOST"],
    port=MONGO["PORT"]
)

# 连接的数据库, 需要哪张表可以在上面的 COLLECTION 字段进行设置
MONGO_DB = CONN[MONGO["DB"]]
# collection mongodb 中的表
COLLECTION = MONGO_DB[MONGO["COLLECTION"]]

# MySQL 设置
MYSQL_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
    host = MYSQL["HOST"],
    port = MYSQL["PORT"],
    database = MYSQL["DB"],
    user = MYSQL["USER"],
    password = MYSQL["PASSWORD"],
)

# 连接redis
REDIS_CONN = redis.Redis(host=REDIS["HOST"], port=REDIS['PORT'])

# session 安全密钥
SECRET_KEY = 'jdsklfjo678*……*5645435njh*NBGF(kv%&^%&$%JK'

# 配置
MAIN_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': MYSQL_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SESSION_TYPE': 'redis',  # session种类
    'SECRET_KEY': SECRET_KEY,
    'SESSION_REDIS': REDIS_CONN,
    'SESSION_KEY_PREFIX': os.path.split(BASE_DIR)[-1],  # 这里是你的项目的名称
}

""" 日志配置 """
LOG_PATH = os.path.join(BASE_DIR, 'logs')
# 不存在目录就配置目录
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

# 日志的文件名，以每天的日期作为名称
LOG_FILE_NAME = datetime.datetime.now().strftime('%Y-%m-%d')

# 日志等级设置
LOG_LEVEL = 'DEBUG'  # 调试
# LEVEL = 'ERROR'  # 错误
# LEVEL = 'WARNING'  # 警告


def start_logging():
    """日志设置"""
    # 业务逻辑已开启就加载日志
    # 设置日志的记录等级
    logging.basicConfig(level=LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/{log_file_name}.log".format(log_file_name=LOG_FILE_NAME),
                                           maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（应用程序实例app使用的）添加日后记录器
    logging.getLogger().addHandler(file_log_handler)
