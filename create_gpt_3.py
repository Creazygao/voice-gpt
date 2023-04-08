import re
import urllib.error
import urllib.request
import openai

# 创建chatgpt 类
class create_gpt3:
    def __init__(self, key):
        self.prompt = '你是聪明可爱的猫娘，认真回答每一个问题'
        self.model = 'text-davinci-003'
        self.max_tokens = 256
        self.user = 'human'
        self.ai = '猫娘'
        self.stop = ['**']
        openai.api_key = key
        openai.proxy = 'http://127.0.0.1:10809'

    def add_user_prompt(self, message):
        self.prompt += "**" + self.user + ":" + message + "**" + self.ai + ":"

    def add_ai_answer(self, message):
        if self.prompt.endswith(':'):
            self.prompt += message

    def get_summary(self):
        self.add_user_prompt("简要总结我们之前的对话内容")
        answer = openai.Completion.create(
            model=self.model,
            prompt=self.prompt,
            temperature=0.8,
            frequency_penalty=0.8,
            max_tokens=self.max_tokens,
            stop=self.stop
        )
        answer_message = answer.choices[0]['text'].strip().replace(r'\n', '')
        self.prompt = "这是之前的对话内容：" + answer_message
        return answer_message

    def get_reply_from_gpt(self, query):
        """
        一般性的问题回答
        :param query: 提问
        :return: gpt3的回答
        """
        if (len(self.prompt) + len(query) + self.max_tokens) > 4094:
            self.get_summary()
        self.add_user_prompt(query)
        answer = openai.Completion.create(
            model=self.model,
            prompt=self.prompt,
            temperature=0.8,
            frequency_penalty=0.8,
            max_tokens=self.max_tokens,
            stop=self.stop
        )
        answer_message = answer.choices[0]['text'].strip().replace(r'\n', '')
        self.add_ai_answer(answer_message)
        return answer_message

    def extract_answer(self, query, text):
        temp_memory = "从网络信息中提取正确信息"
        temp_memory += "**" + self.user + ": " + text + "**" + self.ai + ": "
        answer = openai.Completion.create(
            model=self.model,
            prompt=temp_memory,
            temperature=0.6,
            frequency_penalty=0.2,
            max_tokens=512,
            stop=self.stop
        )
        answer_message = answer.choices[0]['text'].strip().replace(r'\n', '')
        self.add_user_prompt(query)
        self.add_ai_answer(answer_message)
        return answer_message

    def get_news(self, query, news):
        temp_memory = "按顺序,分条进行热搜新闻报道:"
        temp_memory += "**" + self.user + ": " + news + "**" + self.ai + ": "
        answer = openai.Completion.create(
            model=self.model,
            prompt=temp_memory,
            temperature=0.6,
            frequency_penalty=0.2,
            max_tokens=512,
            stop=self.stop
        )
        answer_message = answer.choices[0]['text'].strip().replace(r'\n', '')
        self.add_user_prompt(query)
        self.add_ai_answer(answer_message)
        return answer_message

    def get_weather(self, query,weather_report):
        """
        从open weather获取天气信息
        :param query: 关于天气的提问
        :return: 根据open weather的天气总结
        """
        temp_memory = weather_report
        temp_memory += "**" + self.user + ": " + query + "**" + self.ai + ": "
        answer = openai.Completion.create(
            model=self.model,
            prompt=temp_memory,
            temperature=0.5,
            frequency_penalty=0.2,
            max_tokens=self.max_tokens,
            stop=self.stop
        )
        answer_message = answer.choices[0]['text'].strip().replace(r'\n', '')
        self.add_user_prompt(query)
        self.add_ai_answer(weather_report)
        return answer_message
