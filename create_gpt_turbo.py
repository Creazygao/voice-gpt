import openai


# 创建chatgpt 类
class create_chatgpt:
    def __init__(self, key):
        self.key = key
        self.model = 'gpt-3.5-turbo'
        self.max_tokens = 512
        openai.proxy = "http://127.0.0.1:10809"
        openai.api_key = self.key

    def get_reply(self, message):
        answer = openai.ChatCompletion.create(
            model=self.model,
            messages=message,
            temperature=0.8,
            frequency_penalty=0.8,
            max_tokens=self.max_tokens,
        )
        answer_message = answer['choices'][0]['message']['content']
        return answer_message
