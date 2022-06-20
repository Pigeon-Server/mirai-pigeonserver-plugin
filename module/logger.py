# 日志模块
from loguru import *
import os
import datetime
# 检查是否存在logs文件夹
logs = os.path.join('logs')
if not os.path.exists(logs):
    os.makedirs(logs)
# 创建日志
nowtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
log = logger.add("./logs/output_{time}.log".format(time=nowtime), format="[{time:MM-DD HH:mm:ss}] - {level}: {message}", rotation="00:00", compression="zip")
