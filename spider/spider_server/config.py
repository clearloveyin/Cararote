class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.25.88/new_spider'
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = -1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = 'cache_root'
    HOST = "https://cactus.suntec.net/"
    LOGIN_URL = HOST + "cactuswebapi/auth/login"


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''

class ReleaseConfig(Config):
    pass


config = {
    'development': DevelopConfig,
    'release': ReleaseConfig,
    'default': ReleaseConfig
}
