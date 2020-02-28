# re   xpath   bs4

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_cities():
    url_cities = []
    url = "http://www.tianqihoubao.com/lishi/"
    resp = requests.get(url)
    html = resp.content.decode('gbk')
    # print(resp.text)   # 文本形式返回网页源代码
    # print(resp.content)    # 二进制形式返回网页内容
    # print(resp.content.decode('utf-8'/'gbk'/'gb2312'))    #解码
    soup = BeautifulSoup(html, 'html.parser')  # (html,'lxml')
    # print(soup)
    dd_list = soup.find_all('dd')
    # print(dd_list)
    for dd in dd_list:
        # print(dd)
        a_list = dd.find_all('a')
        for a in a_list:
            # print(a)
            url_cities.append(a['href'].rstrip('.html'))

    # for url_city in url_cities:
    #     print(url_city)

    return url_cities


def get_data(url):
    # 1.
    # url = 'http://tianqihoubao.com/lishi/guangzhou/month/201901.html'
    # 2.
    resp = requests.get(url)
    html = resp.content.decode('gbk')
    # 3.
    # print(resp.text)   # 文本形式返回网页源代码
    # print(resp.content)    # 二进制形式返回网页内容
    # print(resp.content.decode('utf-8'/'gbk'/'gb2312'))    #解码
    soup = BeautifulSoup(html, 'html.parser')  # (html,'lxml')
    # print(soup)
    tr_list = soup.find_all('tr')
    # print(tr_list)
    dates, conditions, temph, templ, wind1, wind2 = [], [], [], [], [], []
    for data in tr_list[1:]:
        sub_data = data.text.split()
        # print(sub_data)
        dates.append(sub_data[0])
        conditions.append(''.join(sub_data[1:3]))
        temph.append(''.join(sub_data[3:4]))
        templ.append(''.join(sub_data[5:6]))
        wind1.append(''.join(sub_data[7:8]))
        wind2.append(''.join(sub_data[9:10]))
    _data = pd.DataFrame()
    _data['日期'] = dates
    _data['天气状况'] = conditions
    _data['最高气温'] = temph
    _data['最低气温'] = templ
    _data['风力1'] = wind1
    _data['风力2'] = wind2

    return _data


cities = get_cities()
# print(cities)
base_url = 'http://www.tianqihoubao.com'
cities_data = []
for city in cities:
    city_data = []
    for year in range(2011, 2012):
        for month in range(1, 13):
            if month < 10:
                url = base_url + city + '/month/' + str(year) + '0' + str(month) + '.html'
            else:
                url = base_url + city + '/month/' + str(year) + str(month) + '.html'
            print(url)
            city_month = get_data(url)
            city_data.append(city_month)
    city_name = city.lstrip('/lishi/') + '.csv'
    print(city_name)
    data = pd.concat(city_data).reset_index(drop=True)
    data.to_csv(city_name, index=False, encoding='utf-8-sig')
    # cities_data.append(pd.concat(city_data).reset_index(drop=True))

# for index in range(0, len(cities_data)):
#     city_name = cities[index] + '.csv'
#     print(city_name)
#     cities_data[index].to_csv(city_name, index=False, encoding='utf-8-sig')

# data_1_month = get_data('http://www.tianqihoubao.com/lishi/shijiazhuang/month/201501.html')
# data_2_month = get_data('http://www.tianqihoubao.com/lishi/shijiazhuang/month/201502.html')
# data_3_month = get_data('http://www.tianqihoubao.com/lishi/shijiazhuang/month/201503.html')
#
# data = pd.concat([data_1_month, data_2_month, data_3_month]).reset_index(drop=True)
# # 4.
# data.to_csv('shijiaz.csv', index=False, encoding='utf-8-sig')
