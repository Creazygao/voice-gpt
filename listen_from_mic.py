import os
from sr_rewrite import myRecognizer
import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def listening_mic(proxy):
    mr = myRecognizer(proxy)
    try:
        with sr.Microphone() as source:
            mr.adjust_for_ambient_noise(source, duration=1)
            logging.info('正在聆听...')
            audio = mr.listen(source)
            logging.info("正在翻译语音...")
            speech_text = mr.recognize_google(audio, language='zh-ch')
            logging.info("翻译结果：" + speech_text)
            return speech_text
    except Exception as e:
        logging.error(e)
        return None
