import requests
from bs4 import BeautifulSoup

url_cities = []
cities = []
url = "http://www.tianqihoubao.com/lishi/"
resp = requests.get(url)
html = resp.content.decode('gbk')
print(resp)
print(resp.text)   # 文本形式返回网页源代码
# print(resp.content)    # 二进制形式返回网页内容
# print(resp.content.decode('utf-8'/'gbk'/'gb2312'))    #解码
soup = BeautifulSoup(html, 'html.parser')  # (html,'lxml')
print(soup)
dd_list = soup.find_all('dd')
# print(dd_list)
for dd in dd_list:
    # print(dd)
    a_list = dd.find_all('a')
    for a in a_list:
        # print(a)
        url_cities.append(a['href'].rstrip('.html'))
        cities.append(a.string)

for url_city in url_cities:
    print(url_city)

for city in cities:
    print(city)
