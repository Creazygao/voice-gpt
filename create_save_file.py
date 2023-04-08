import time
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def create_file():
    """
    根据当前日期创建音频的保存目录
    :return: 文件夹的地址
    """
    now = datetime.now()
    today = f'{now.month}-{now.day}-{now.year}'
    try:
        if not os.path.isdir(f'./record'):
            os.mkdir(f'./record')
        if not os.path.isdir(f'./record/{today}'):
            os.mkdir(f'./record/{today}')
        file_dir = f'./record/{today}/'
        return file_dir
    except Exception as e:
        logging.error(e)
        return None
