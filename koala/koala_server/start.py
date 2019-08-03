# -*- coding: UTF-8 -*-
from app import create_app
import os
import logging
import logging.handlers

app = create_app('default')

info_log = os.path.join('log', 'weblog.log')
info_file_handler = logging.handlers.RotatingFileHandler(
    info_log, maxBytes=1048576, backupCount=20)
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                      '[in %(pathname)s:%(lineno)d]')
)
app.logger.addHandler(info_file_handler)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=5000)
    #app.run(debug=True, host='', port=25000, threaded=True)
