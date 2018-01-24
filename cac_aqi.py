#! /usr/bin/env python
#-*-coding:utf-8-*-  

#Author : Jackie & Amy
#Get IAQI value from defirrent data
#Date : 2018-01-23
#
#Function getIAQI(airtype, value)
#
#return INT value(round)

import math
from enum import Enum

class AIR_TYPE(Enum):
    SO2 = 1
    NO2 = 2
    PM10 = 3
    O3 = 4
    PM25 = 5
aqi_list = [0, 50, 100, 150, 200, 300, 400, 500]
so2_list = [0, 50, 150, 475, 800, 1600, 2100, 2620]
no2_list = [0, 40, 80,  180, 280, 565, 750, 940]
pm10_list= [0, 50, 150, 250, 350, 420, 500, 600]
o3_list  = [0, 160, 200,300, 400, 800, 1000, 1200]
pm25_list= [0, 35, 75, 115,  150, 250, 350,  500]

def getAQI(value, alist):
	for index, key in enumerate(alist):
		if value <= key:
			break

	#now index saved the ValueIndex
	if index==0:
		return 0
	else:
		il= aqi_list[index-1]
		ih= aqi_list[index]
		ch= alist[index]
		cl= alist[index-1]
		return round(il + (ih-il)*(value-cl)/(ch-cl))
	

def getIAQI(airtype, value):
	if airtype == AIR_TYPE.NO2:	return getAQI(value, no2_list)
	if airtype == AIR_TYPE.SO2:	return getAQI(value, so2_list)
	if airtype == AIR_TYPE.PM10:return getAQI(value, pm10_list)
	if airtype == AIR_TYPE.PM25:return getAQI(value, pm25_list)
	if airtype == AIR_TYPE.O3:	return getAQI(value, o3_list)


############################# downCode is abandon ##############################

# SO2 translate to IAQI
def get_so2_aqi(value):
	if value <=0:
		return 0
	elif value<=50:
		return round(value)
	elif value>50 and value<=150:
		return round((value-50)*50/100 + 50)
	elif value>150 and value<=475:
		return round((value-150)*50/(475-150) + 100)
	elif value>475 and value<=800:
		return round((value-475)*50/(800-475) + 150)
	elif value>800 and value<=1600:
		return round((value-800)*100/(1600-800) + 200)
	elif value>1600 and value<=2100:
		return round((value-1600)*100/(2100-1600) + 300)
	elif value>2100 and value<=2620:
		return round((value-2100)*100/(2620-2100) + 400)
	else:
		return 500

# NO2 translate to IAQI
def get_no2_aqi(value):
	if value<=0:
		return 0
	elif value>0 and value<=40:
		return round((value)*50/40)
	elif value>40 and value<=80:
		return round((value-40)*50/40 + 50)
	elif value>80 and value<=180:
		return round((value-80)*50/(180-80) + 100)
	elif value>180 and value<=280:
		return round((value-180)*50/(280-180) + 150)
	elif value>280 and value<=565:
		return round((value-280)*100/(565-280) + 200)
	elif value>565 and value<=750:
		return round((value-565)*100/(750-565) + 300)
	elif value>750 and value<=940:
		return round((value-750)*100/(940-750) + 400)
	else:
		return 500

# PM10 translate to IAQI
def get_pm10_aqi(value):
	if value<=0:
		return 0
	elif value>0 and value<=50:
		return round((value))
	elif value>50 and value<=150:
		return round((value-50)*50/(150-50) + 50)
	elif value>150 and value<=250:
		return round((value-150)*50/(250-150) + 100)
	elif value>250 and value<=350:
		return round((value-250)*50/(350-250) + 150)
	elif value>350 and value<=420:
		return round((value-350)*100/(420-350) + 200)
	elif value>420 and value<=500:
		return round((value-420)*100/(500-420) + 300)
	elif value>500 and value<=600:
		return round((value-500)*100/(600-500) + 400)
	else:
		return 500

def get_o3_aqi(value):
	if value<=0:
		return 0
	elif value>0 and value<=160:
		return round((value)*50/(160))
	elif value>160 and value<=200:
		return round((value-160)*50/(200-160) + 50)
	elif value>200 and value<=300:
		return round((value-200)*50/(300-200) + 100)
	elif value>300 and value<=400:
		return round((value-300)*50/(400-300) + 150)
	elif value>400 and value<=800:
		return round((value-400)*100/(800-400) + 200)
	elif value>800 and value<=1000:
		return round((value-800)*100/(1000-800) + 300)
	elif value>1000 and value<=1200:
		return round((value-1000)*100/(1200-1000) + 400)
	else:
		return 500

def get_pm25_aqi(value):
	if value<=0:
		return 0
	elif value>0 and value<=35:
		return round((value)*50/(35))
	elif value>35 and value<=75:
		return round((value-35)*50/(75-35) + 50)
	elif value>75 and value<=115:
		return round((value-75)*50/(115-75) + 100)
	elif value>115 and value<=150:
		return round((value-115)*50/(150-115) + 150)
	elif value>150 and value<=250:
		return round((value-150)*100/(250-150) + 200)
	elif value>250 and value<=350:
		return round((value-250)*100/(350-250) + 300)
	elif value>350 and value<=500:
		return round((value-350)*100/(500-350) + 400)
	else:
		return 500




if __name__ == '__main__':
	print(getIAQI(AIR_TYPE.PM10, 144))
	print(getIAQI(AIR_TYPE.PM25, 33))
'''
print(get_so2_aqi(100))
print(get_no2_aqi(280))
print(get_pm10_aqi(300))
print(get_pm25_aqi(72))
print(getIAQI(AIR_TYPE.SO2, 100))
print(getIAQI(AIR_TYPE.NO2, 280))
print(getIAQI(AIR_TYPE.PM10, 300))
print(getIAQI(AIR_TYPE.PM25, 72))
'''

