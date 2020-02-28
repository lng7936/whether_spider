# re   xpath   bs4

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(url, city_name):
    # 1.
    # url = 'http://tianqihoubao.com/aqi/shijiazhuang-201909.html'
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
    h4 = soup.find_all('h4')
    print(tr_list)
    print(h4)
    city, dates, level, aqi, pm25, pm10, so2, no2, co, o3 = [], [], [], [], [], [], [], [], [], []
    for data in tr_list[1:]:
        sub_data = data.text.split()
        print(sub_data)
        city.append(city_name)
        dates.append(sub_data[0])
        level.append(''.join(sub_data[1:2]))
        aqi.append(''.join(sub_data[2:3]))
        pm25.append(''.join(sub_data[4:5]))
        pm10.append(''.join(sub_data[5:6]))
        so2.append(''.join(sub_data[6:7]))
        no2.append(''.join(sub_data[7:8]))
        co.append(''.join(sub_data[8:9]))
        o3.append(''.join(sub_data[9:10]))
    _data = pd.DataFrame()
    _data['城市'] = city
    _data['日期'] = dates
    _data['质量等级'] = level
    _data['aqi'] = aqi
    _data['pm25'] = pm25
    _data['pm10'] = pm10
    _data['so2'] = so2
    _data['no2'] = no2
    _data['co'] = co
    _data['o3'] = o3

    return _data


data_1_month = get_data('http://tianqihoubao.com/aqi/shijiazhuang-201909.html', '石家庄')
data_2_month = get_data('http://tianqihoubao.com/aqi/shijiazhuang-201910.html', '石家庄')
data_3_month = get_data('http://tianqihoubao.com/aqi/shijiazhuang-201911.html', '石家庄')

data=pd.concat([data_1_month,data_2_month,data_3_month,]).reset_index(drop=True)
#4.
data.to_csv('shijiaz.csv',index=False,encoding='utf-8-sig')
