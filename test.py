from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

def get_weather(city):
    # 获取当前日期和时间
    now = datetime.datetime.now()
    now_time=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    # 创建一个 Chrome 浏览器实例
    # browser = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    keyword = city
    url = f"https://www.baidu.com/s?wd={keyword}"
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="1"]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/span')))

    # 打开要爬取的页面 selector.xpath

    # url = 'https://www.bing.com/search?q=北京天气'
    element.click()
    # 等待页面加载完成
    # 获取页面源码
    html = browser.page_source
    # 使用 Beautiful Soup 解析页面数据
    soup = BeautifulSoup(html, 'html.parser')
    time_info = soup.find_all('div', {'class': 'time_3YlZ3'})[1:9]
    tem_info = soup.find_all('div', {'class': 'item_1QXjg cu-color-white'})[1:9]
    now_tem = "现在气温" + soup.find('div', {'class': 'weather-main-temp_1FJag'}).text
    now_weather = '当前天气' + soup.find('span', {'class': 'cu-mr-base'}).text
    now_wind = '风力' + soup.find('span', {'class': 'cu-mr-base'}).find_next_sibling('span').text
    all_tem = '全天气温' + soup.find('span', {'class': 'temp_1ShYr cu-mr-base'}).text
    advice = soup.find('div', {'class': 'pc_5QPD0'}).text
    next_days_weather = soup.find_all('div', {'class': 'list-item_7N2BX WA_LOG_OTHER'})[1:]
    time_array = []
    tem_array = []
    next_day_weather=[]
    for v in time_info:
        time_array.append(v.text.strip().replace('\n', ''))
    for v in next_days_weather:
        next_day_weather.append(v.text.strip().replace('/', '月').replace('\n','').replace('°','到',1))
    for v in tem_info:
        v = v.text.strip().replace('\n', '')
        if '%' not in v:
            v = "0%" + v
        v = v.replace("%", "%的概率有雨、空气质量:").replace('°', '、气温:', 1)
        tem_array.append(v)
    next_weather = dict(zip(time_array, tem_array))
    # 关闭浏览器实例
    weather_report="现在时间是："+now_time+","+now_tem+","+all_tem+\
                   ","+now_wind+","+now_weather+","+"接下来12小时天气为:"\
                   +next_weather+"建议："+advice+",最近4天天气为："+next_day_weather
    browser.quit()
    return weather_report