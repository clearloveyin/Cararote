# -*- coding: UTF-8 -*-
import platform
import os.path
import configparser
cp = configparser.ConfigParser()
cp.read('config.cfg')


class Config:
    if 'RELEASE_DB_HOST' in os.environ:
        DB_HOST = os.environ['RELEASE_DB_HOST']
    else:
        DB_HOST = cp.get('release', 'DB_HOST')
    if 'RELEASE_DB_USER' in os.environ:
        DB_USER = os.environ['RELEASE_DB_USER']
    else:
        DB_USER = cp.get('release', 'DB_USER')
    if 'RELEASE_DB_PASSWD' in os.environ:
        DB_PASSWD = os.environ['RELEASE_DB_PASSWD']
    else:
        DB_PASSWD = cp.get('release', 'DB_PASSWD')
    if 'RELEASE_DB_NAME' in os.environ:
        DB_NAME = os.environ['RELEASE_DB_NAME']
    else:
        DB_NAME = cp.get('release', 'DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (DB_USER, DB_PASSWD, DB_HOST, DB_NAME)
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = -1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LDAP_PROVIDER_URL = 'LDAP://apolo.storm'
    LDAP_DOMAIN = 'storm'
    # ARCHITECTURE_SRV = 'http://192.168.8.152/'  # 框架服务器地址
    # FILE_SRV_URL = 'http://192.168.25.99:8081'
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = 'cache_root'
    SALES_ROLE_ID = 1
    SGL_ROLE_ID = 2
    GL_ROLE_ID = 3
    SUPER_PL_ROLE_ID = 4
    SALES_STATUS_LIST = ["新建", "处理中", "确认中", "已提出", "已承认"]
    SGL_STATUS_LIST = ["新建", "处理中", "确认中", "已提出"]
    GL_STATUS_LIST = ["新建", "处理中", "确认中"]
    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(Config):
    if 'DEVELOP_DB_HOST' in os.environ:
        DB_HOST = os.environ['DEVELOP_DB_HOST']
    else:
        DB_HOST = cp.get('development', 'DB_HOST')
    if 'DEVELOP_DB_USER' in os.environ:
        DB_USER = os.environ['DEVELOP_DB_USER']
    else:
        DB_USER = cp.get('development', 'DB_USER')
    if 'DEVELOP_DB_PASSWD' in os.environ:
        DB_PASSWD = os.environ['DEVELOP_DB_PASSWD']
    else:
        DB_PASSWD = cp.get('development', 'DB_PASSWD')
    if 'DEVELOP_DB_NAME' in os.environ:
        DB_NAME = os.environ['DEVELOP_DB_NAME']
    else:
        DB_NAME = cp.get('development', 'DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (DB_USER, DB_PASSWD, DB_HOST, DB_NAME)
    if 'DEVELOP_CACTUS_URL' in os.environ:
        HOST = os.environ['DEVELOP_CACTUS_URL']
    else:
        HOST = cp.get('development', 'DEVELOP_CACTUS_URL')
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    # if platform.system() == 'Windows':
    #     # Z盘映射地址：\\192.168.64.128\data
    #     SPEC_PATH_ROOT = os.path.join(r'Z:\Input')
    #     SPEC_PATH_TEMP = os.path.join(r'Z:\Input\temp')
    #     FILE_SRV_URL = 'http://192.168.25.99:8081'
    #     SPEC_CHANGE_URL = os.path.join(r'Z:')
    # else:
    #     SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Input')
    #     SPEC_PATH_TEMP = os.path.join(os.path.expanduser('~'), 'data', 'Input', 'temp')
    #     FILE_SRV_URL = 'http://192.168.25.99:8081'
    #     SPEC_CHANGE_URL = os.path.join(os.path.expanduser('~'), 'data')


class ReleaseConfig(Config):
    if 'RELEASE_CACTUS_URL' in os.environ:
        HOST = os.environ['RELEASE_CACTUS_URL']
    else:
        HOST = cp.get('release', 'RELEASE_CACTUS_URL')
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    # if platform.system() == 'Windows':
    #     # R盘映射地址：\\192.168.68.135\data
    #     SPEC_PATH_TEMP = os.path.join(r'R:\Input\temp')
    #     SPEC_PATH_ROOT = os.path.join(r'R:\Input')
    #     FILE_SRV_URL = 'http://192.168.25.46'
    #     SPEC_CHANGE_URL = os.path.join(r'Z:')
    # else:
    #     SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Input')
    #     SPEC_PATH_TEMP = os.path.join(os.path.expanduser('~'), 'data', 'Input', 'temp')
    #     FILE_SRV_URL = 'http://192.168.25.46'
    #     SPEC_CHANGE_URL = os.path.join(os.path.expanduser('~'), 'data')


config = {
    'development': DevelopConfig,
    'release': ReleaseConfig,
    'default': ReleaseConfig
}
