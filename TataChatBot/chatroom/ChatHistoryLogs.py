import os
import logging
from logging.handlers import TimedRotatingFileHandler
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# format the log entries
print("base dir of logger @@@@@@@@@",base_dir)
formatter = logging.Formatter('%(asctime)s  %(message)s')

handler = TimedRotatingFileHandler(str(base_dir)+'/chatroom/logs/chat_history.log', when='midnight', backupCount=180)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)