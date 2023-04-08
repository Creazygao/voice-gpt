# coding=utf-8
import logging
import sys
import json
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus

PER = 5118
SPD = 5
PIT = 5
VOL = 5
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON972348"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'


def fetch_token(API_KEY, SECRET_KEY):
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def get_baidu_voice(TEXT, save_file, api_key, secret_key):
    token = fetch_token(api_key, secret_key)
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except  URLError as err:
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else save_file
    try:
        with open(save_file, 'wb') as of:
            of.write(result_str)
            return True
    except Exception as e:
        logging.error(e)
        return None

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
            logging.error(result_str)
            return None


def text_to_voice_baidu(text, file_path, query, api_key, secret_key):
    """
    使用百度 tts将文本转化为声音
    :param text: 文本
    :param speech_text:保存的声音文件的名称
    :return:
    """
    plain_text = re.sub('([^\u4e00-\u9fa5])', '', query)
    filename = file_path + plain_text + ".mp3"
    try:
        get_baidu_voice(text, filename, api_key, secret_key)
        return filename
    except Exception as e:
        logging.info(e)
        return None
