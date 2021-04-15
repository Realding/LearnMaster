# This is setting file to config flask server
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
# Database setting
databases = {
    "sqlite": {
        "driver": "sqlite",
        "database": os.path.join(base_dir, "sqlite.db")
    },

    "mysql": {
        "driver": "mysql+pymysql",
        "user": "root",
        "password": "123456",
        "host": "127.0.0.1",
        "port": "3306",
        "database": "test",
    }
}
sqlite_url_format = '{driver}:///{database}'
mysql_url_format = '{driver}://{user}:{password}@{host}:{port}/{database}'


# Flask setting
class Config:
    SECRET_KEY = 'key_string'
    SQLALCHEMY_BINDS = {
        'sqlite': sqlite_url_format.format(**databases['sqlite']),
        'mysql': mysql_url_format.format(**databases['mysql'])
    }
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_BINDS['sqlite']
    # 便于调试
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
    # 调试模式
    DEBUG = True
    # 支持返回中文JSON
    JSON_AS_ASCII = False
    # JSONIFY_MIMETYPE = "text/plain;charset=UTF-8"

