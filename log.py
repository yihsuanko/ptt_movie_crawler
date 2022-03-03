import logging

logger = logging.getLogger()  # 設置root logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler輸出到file
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# 使用StreamHandler輸出到console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# 使用兩個Handler
logger.addHandler(ch)
logger.addHandler(fh)
logger.info('this is info message')
logger.warn('this is warn message')