from flask import Flask
from flask_restful import Api
from flask_cors import *
from config import config
from app.api_1_0 import Api_1_0
from app.db import db, cache
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {'class': 'logging.StreamHandler',
                    # 'stream': 'ext: // sys.stdout',
                    'formatter': 'default'
                    },
        'file': {'class': 'logging.FileHandler',
                 'level': 'DEBUG',
                 'formatter': 'default',
                 'filename': 'log/systemlog.log'
                 }
    },
    # 'loggers': {
    #     'wsgi': {'level': 'DEBUG',
    #                 'handlers': '[wsgi]',
    #                 'propagate': 'no'
    #                 },
    #     'file': {'level': 'DEBUG',
    #              'handlers': '[file]',
    #              'propagate': 'no'
    #              }
    # },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    cache.init_app(app)
    db.init_app(app)
    api = Api()
    Api_1_0(api)
    api.init_app(app)
    CORS(app, supports_credentials=True)
    # print(app.url_map)
    return app




