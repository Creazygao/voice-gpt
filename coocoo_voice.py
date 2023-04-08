import os
import sys
import threading
import logging
import pygame
from listen_from_mic import listening_mic
from read_evn_args import get_args
from create_save_file import create_file
from baidu_voice import text_to_voice_baidu
from answer_from_web import get_answer_from_web
from create_gpt_3 import create_gpt3
from weather import get_weather
from news import get_news
from create_gpt_turbo import create_chatgpt

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def play_voice(file_path, mixer):
    """
    播放 指定的音频文件
    :param file_path: 音频文件路径
    :param music: pygame的mixer.music对象
    :return: 音频文件长度
    """
    sound = mixer.Sound(file_path)
    time_length = mixer.Sound(file_path).get_length()
    sound.play()
    return time_length


def wrap_message(role, message):
    return {'role': role, 'content': message}


if __name__ == '__main__':
    working = True
    listening = 3
    net_keywords = ['查', '最新', '最近']
    pygame.init()
    pygame.mixer.init()
    args = get_args()
    chatgpt = create_gpt3(args["OPENAI_KEY"])
    today_news = get_news()

    try:
        # 读取环境变量
        api_key = args["BAIDU_VOICE_API_KEY"]
        secret_key = args["BAIDU_VOICE_SECRET_KEY"]
        if args is None:
            logging.error("参数读取错误，请配置coocoo.env文件")
            sys.exit()
        # 创建保存语音文件夹
        file_dir = create_file()
        if file_dir is None:
            logging.error("文件夹创建失败，请检查/record文件夹权限")
            sys.exit()
        # 程序启动问候语
        logging.info("开始语音对话：")
        # 初始化pygame
        voice_path = text_to_voice_baidu("你好", file_dir, "问候", api_key, secret_key)
        if voice_path is not None:
            print(voice_path)
            logging.info("Coocoo:你好，我是Coocoo")
            play_voice(voice_path, pygame.mixer)
            while pygame.mixer.get_busy():
                pygame.time.Clock().tick(10)
        else:
            logging.info("没有返回音频文件，请检查百度语音API")
            sys.exit()
        # 开始主循环
        while working:
            speech_text = listening_mic(args["PROXY"])
            if speech_text is None:
                continue
            if pygame.mixer.get_busy():
                # 如果听到’停下‘关键词，就停止播放
                if '停下' in speech_text:
                    pygame.mixer.stop()
            elif '退出' in speech_text:
                working = False
            elif '拜拜' in speech_text:
                listening = 0
                voice_path = text_to_voice_baidu("好的，我先去休息了", file_dir, speech_text, api_key, secret_key)
                logging.info("Coocoo:好的，我先去休息了")
                play_voice(voice_path, pygame.mixer)
            # 联网搜索信息
            elif any(keyword in speech_text for keyword in net_keywords):
                speech_text = speech_text.strip().replace('\n', '')
                answer = get_answer_from_web(speech_text)
                logging.info(answer)
                reply = chatgpt.extract_answer(speech_text, speech_text + ",请从下面网页搜索结果中提取信息，并给出最合适的答案：  " + answer)
                logging.info('Coocoo:' + reply)
                voice_path = text_to_voice_baidu(reply, file_dir, speech_text, api_key, secret_key)
                play_voice(voice_path, pygame.mixer)
            # 搜索热搜新闻
            elif '新闻' in speech_text:
                logging.info(today_news)
                # reply = chatgpt.get_news(speech_text, "按顺序进行热搜新闻报道：  " + today_news)
                # logging.info('Coocoo:' + reply)
                voice_path = text_to_voice_baidu("今天的热搜新闻有：" + today_news, file_dir, speech_text, api_key, secret_key)
                play_voice(voice_path, pygame.mixer)
            # 搜索天气
            elif '天气' in speech_text:
                weather_report = get_weather(speech_text)
                # 从网站爬取天气信息
                if weather_report is None:
                    voice_path = text_to_voice_baidu("未查询到天气，是不是丫丫听错了？", file_dir, speech_text, api_key, secret_key)
                    play_voice(voice_path, pygame.mixer)
                    continue
                reply = chatgpt.get_weather(speech_text, weather_report)
                logging.info('Coocoo:' + reply)
                voice_path = text_to_voice_baidu(reply, file_dir, speech_text, api_key, secret_key)
                play_voice(voice_path, pygame.mixer)
                # “在吗”为唤醒词,设置flag>0,以激活self.flag>0的条件，进行回复
            elif "在吗" in speech_text:
                listening = 3
                text_to_voice_baidu("在的在的", file_dir, speech_text, api_key, secret_key)
                logging.info('Coocoo:' + '在的在的')
                # 当flag>0时，使用gpt进行回复，如果flag<0，则gpt不回复
            elif listening > 0:
                reply = chatgpt.get_reply_from_gpt(speech_text)
                logging.info('Coocoo:' + reply)
                text_to_voice_baidu(reply, file_dir, speech_text, api_key, secret_key)

    except Exception as e:
        logging.error(e)
