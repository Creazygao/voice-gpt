import requests
from bs4 import BeautifulSoup


def get_news():
    url = 'http://top.baidu.com/board?tab=realtime'

    # 发送 GET 请求
    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 100.0.4896.127Safari / 537.36"
    }  #
    response = requests.get(url, headers=head)

    # 解析 HTML 代码
    soup = BeautifulSoup(response.text, 'html.parser')
    texts = soup.find_all('div', {'class': 'category-wrap_iQLoo horizontal_1eKyQ'})
    hot_news = []
    for cont in texts:
        title = cont.find('div', {'class': 'c-single-text-ellipsis'}).text.strip()
        content = cont.find('div', {'class': 'large_nSuFU'}).text.strip().replace('查看更多>', '')
        hot_news.append({title})

        # hot_news.append({str(title.text): str(content.text)})
    hot_news=hot_news[1:15]
    return str(hot_news).replace('[', '').replace(']', '').replace('\'',
           '').replace(',', '').replace('{', '').replace('}', '。').strip()
