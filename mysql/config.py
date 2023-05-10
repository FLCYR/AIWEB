
class BaseConfig(object):

    # 数据库的配置
    DIALCT = "mysql"
    DRITVER = "pymysql"
    HOST = '39.108.71.11'
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "123456"
    DBNAME = 'asserts'

    SQLALCHEMY_DATABASE_URI = f"{DIALCT}+{DRITVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    # EMAIL的配置

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '15768727342@163.com'
    MAIL_PASSWORD = 'UZNJOPDEJOMXDXUO'
    MAIL_DEFAULT_SENDER = ' '
