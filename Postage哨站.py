# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:33:20 2022

@author: PhoenixWANG
contact_email:shadowdouble76@gmail.com
contact_number:+852 59310375,+86 13081609607
"""
import urllib.request
import camelot
import pandas as pd
import json
import requests
import geocoder
from math import radians,cos,sin,asin,sqrt

street_name = input('请输入街道名称：（中文，英文均可）\n')
street_number = input('请输入对应屋宇号码（如，您的地址是甲乙路一号，那么这里输入‘1’）')


#下载文档
url_1 = "https://www.chp.gov.hk/files/pdf/"+"building_list_eng.pdf"
response = urllib.request.urlopen(url_1)
file_1 = open("确诊大厦.pdf",'wb')
file_1.write(response.read())
file_1.close()

#解析文档
table_1 = camelot.read_pdf("确诊大厦.pdf",pages = '1-end',flavor = 'stream')
table_1_length = table_1.n
table_1_list = pd.DataFrame()
table_1_list = (table_1[0].df).append(table_1[1].df)
for i in range(table_1_length-2):
    table_1_list = table_1_list.append(table_1[i].df)
table_1_list = table_1_list[(table_1_list[0]=='Kowloon City')]


#提取有关地点GPS位置
#code from Youtube:
parameters = {
    "key":"KguPtEMuVb5f6eICr3zRLN1TDFtY1Rek",#免费的API，这是我的，你也可以自己去申请一个
    "location":"Des Voeux Road West 224-226,000000,HongKong"#记得换成目标的GPS经纬度阵列,该位置为确诊的德辅道西224-226号
    }
response = requests.get("http://www.mapquestapi.com/geocoding/v1/address",params = parameters)
data = json.loads(response.text)['results']
lat = data[0]['locations'][0]['latLng']['lat']
lng = data[0]['locations'][0]['latLng']['lng']
#print(lat,lng)

#获取当前设备所在的经纬度
mylocation = street_name+' '+street_number
my_parameters = {
    "key":"KguPtEMuVb5f6eICr3zRLN1TDFtY1Rek",
    "location":mylocation+",000000,HongKong"#这是你自己的位置
    }
my_response = requests.get("http://www.mapquestapi.com/geocoding/v1/address",params = my_parameters)
myloc = json.loads(my_response.text)['results']
mylat = myloc[0]['locations'][0]['latLng']['lat']
mylng = myloc[0]['locations'][0]['latLng']['lng']

#计算有关地点距离当前的距离
def distance_calculation(lat,lng,mylat,mylng):
    lat,lng,mylat,mylng = map(radians,[float(lat),float(lng),float(mylat),float(mylng)])
    dlat = lat-mylat
    dlng = lng-mylng
    a = sin(dlat/2)**2+cos(lat)*cos(mylat)*sin(dlng/2)**2
    distance = 2*asin(sqrt(a))*6371*1000
    distance = round(distance/1000,3)
    return distance

#数据生成
distance = distance_calculation(lat,lng,mylat,mylng)
print("确诊的大楼位置: "+ str(lat) + ',' + str(lng))
print("你的位置" + str(mylat) + ',' + str(mylng))
print("你们之间的距离是" + str(distance) + '公里')

#设定警戒阈值，我也不知道感染源距离你的直线距离大于多少才算安全

#如果低于警戒阈值，发出提醒并输出对应确诊大楼的位置信息（街道名称与号码）
