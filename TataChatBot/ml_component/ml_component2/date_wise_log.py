#import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# format the log entries
print("base dir of logger @@@@@@@@@",base_dir)
formatter = logging.Formatter('%(asctime)s  %(message)s')

handler = TimedRotatingFileHandler(str(base_dir)+'/logs/my_app.log', when='midnight', backupCount=180)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Ml_LOGFILE_NAME = str(base_dir)+'/log/Ml_errors.log'
# LOGFILE_SIZE = 5 * 1024 * 1024
# LOGFILE_COUNT = 5
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '[%(asctime)s] %(levelname)s %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#         'verbose': {
#             'format': '[%(asctime)s] %(levelname)s ' + ' [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#     },
#     'handlers': {
#         'eguru_log': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'maxBytes': LOGFILE_SIZE,
#             'backupCount': LOGFILE_COUNT,
#             'filename': Ml_LOGFILE_NAME,
#             'formatter': 'simple'
#         }
#     }
# }

# generate example messages
# for i in range(10000):
#     time.sleep(1)
#     logger.debug('debug message')
#     logger.info('informational message')
#     logger.warn('warning')
#     logger.error('error message')
#     logger.critical('critical failure')