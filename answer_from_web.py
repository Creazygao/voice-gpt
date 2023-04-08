import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def search_bing(keyword):
    url = 'https://bing.com/search?q='
    url = url + keyword

    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 100.0.4896.127Safari / 537.36"
    }

    response = requests.get(url, headers=head)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="b_algo")
        res = []
        for result in results:
            try:
                title = result.find("h2").text.strip()
                link = result.find("a")["href"].strip()
                abstract = result.find("div", class_="b_caption").find("p").text.strip()
                if len(res) < 5:
                    res.append(abstract)
            except Exception as e:
                pass
        return res
    else:
        return "error"


def get_answer_from_web(keyword):
    results = search_bing(keyword)
    res = str(results).strip().replace("\n", '')
    return res
