import argparse
import logging
import os
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--OPENAI_KEY", type=str, help="OpenAI API key")
    parser.add_argument("--PROXY", type=str, help="Proxy server URL")
    parser.add_argument("--GOOGLE_VOICE_KEY", type=str, help="Google Cloud Text-to-Speech API key")
    parser.add_argument("--BAIDU_VOICE_API_KEY", type=str, help="Baidu Speech Recognition API key")
    parser.add_argument("--BAIDU_VOICE_SECRET_KEY", type=str, help="Baidu Speech Recognition secret key")
    args = parser.parse_args()

    env_vars = {}
    with open("coocoo.env") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            var_name, var_value = line.split("=", 1)
            env_vars[var_name] = var_value

    result = {}
    for arg in ["OPENAI_KEY", "PROXY", "GOOGLE_VOICE_KEY", "BAIDU_VOICE_API_KEY", "BAIDU_VOICE_SECRET_KEY"]:
        if getattr(args, arg):
            result[arg] = getattr(args, arg)
        elif arg in env_vars:
            result[arg] = env_vars[arg]
        else:
            logging.ERROR(f"Error: {arg} is missing. Please provide it via command line argument or in coocoo.env file.")
            return None

        # 检查参数值是否为空，如果为空则返回提醒
        if result[arg] == "":
            logging.ERROR(f"Error: {arg} value is empty. Please provide a non-empty value.")
            return None

    return result
