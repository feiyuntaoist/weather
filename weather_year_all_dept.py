#! /usr/bin/env python
#-*-coding:utf-8-*-  
# modify INPUT_MONTH PARAM

#Author : Jackie & Amy
#Date : 2018-01-28

import os
import re
import csv
import math
import cac_aqi

from collections import Counter
import numpy
import matplotlib.pyplot as plt
from pylab import mpl

#input MONTH
INPUT_MONTH = '2017'
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#readData col number
DEPT_STR = '东四,天坛,官园,万寿西宫,奥体中心,农展馆,万柳,北部新区,植物园,丰台花园,云岗,古城,房山,大兴,亦庄,通州,顺义,昌平,门头沟,平谷,怀柔,密云,延庆,定陵,八达岭,密云水库,东高村,永乐店,榆垡,琉璃河,前门,永定门内,西直门北,南三环,东四环'
COL_NUM = 35
# save the days
days_list = []
days_set = set()

#save PM_data for the month
aqi_dict = {}
aqi_count = {}
so2_dict = {}
so2_count = {}
no2_dict = {}
no2_count = {}
pm10_dict = {}
pm10_count = {}
o3_dict = {}
o3_count = {}
pm25_dict = {}
pm25_count = {}

filename1 = './beijing_20170101-20171231/beijing_all_20170108.csv'
filename2 = './beijing_20170101-20171231/beijing_extra_20170108.csv'

def eachFile(filepath):
	patternxml = r'.*' + INPUT_MONTH + '.*\.csv'
	with os.scandir(filepath) as it:
		for entry in it:
			if not entry.name.startswith('.') and entry.is_file():
				if (re.match(patternxml, entry.name)):
					yield entry.path

def is_number(num):
	try:
		int(num)
		return True
	except ValueError:
		return False

def readRow(row, sum_list, count_list):
	for i in range(COL_NUM):
		if is_number(row[i+3]):
			sum_list[i] += int(row[i+3])
			count_list[i] +=1

def readAddFile(filename): 
	global aqi_dict, pm10_dict, pm25_dict, aqi_count, pm10_count, pm25_count
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		header_row = next(reader)

		#if len is short then the file is not valid
		if len(header_row) != COL_NUM + 3:
			return False
		
		#save indeed row real data
		row_cac_aqi_count_list = [0 for x in range(0, COL_NUM)]
		row_cac_pm10_count_list = row_cac_aqi_count_list[:]
		row_cac_pm25_count_list = row_cac_aqi_count_list[:]

		#save indeed pm25 data
		sum_aqi_list = row_cac_aqi_count_list[:]
		sum_pm10_list = row_cac_aqi_count_list[:]
		sum_pm25_list = row_cac_aqi_count_list[:]

		# read data from every_row
		for row in reader:
			if len(row) > 10:   # this sentance is not sure
				day = row[0][0:8]  #cut the year-month-day
				#read AQI
				if row[2] == 'AQI':	readRow(row, sum_aqi_list, row_cac_aqi_count_list)
				#read pm10
				if row[2] == 'PM10':	readRow(row, sum_pm10_list, row_cac_pm10_count_list)
				#read PM2.5
				if row[2] == 'PM2.5':	readRow(row, sum_pm25_list, row_cac_pm25_count_list)

		days_set.add(day)
		#AQI make average value, but the other get sum_count
		aqi_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_aqi_list, row_cac_aqi_count_list))
		pm10_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_pm10_list, row_cac_pm10_count_list))
		pm25_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_pm25_list, row_cac_pm25_count_list))

def readExtraFile(filename): 
	global so2_dict, no2_dict, o3_dict, so2_count, no2_count, o3_count
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		header_row = next(reader)

		#if len is short then the file is not valid
		if len(header_row) != COL_NUM + 3:
			return False
		
		#save indeed row real data
		row_cac_so2_count_list =  [0 for x in range(0, COL_NUM)]
		row_cac_no2_count_list = row_cac_so2_count_list[:]
		row_cac_o3_count_list = row_cac_so2_count_list[:]

		#save indeed pm25 data
		sum_so2_list = row_cac_so2_count_list[:]
		sum_no2_list = row_cac_so2_count_list[:]
		sum_o3_list = row_cac_so2_count_list[:]

		# read data from every_row
		for row in reader:
			if len(row) > 10:   # this sentance is not sure
				day = row[0][0:8]  #cut the day
				#read so2
				if row[2] == 'SO2':	readRow(row, sum_so2_list, row_cac_so2_count_list)
				#read NO2
				if row[2] == 'NO2':	readRow(row, sum_no2_list, row_cac_no2_count_list)
				#read o3
				if row[2] == 'O3':	readRow(row, sum_o3_list, row_cac_o3_count_list)

		days_set.add(day)
		so2_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_so2_list, row_cac_so2_count_list))
		no2_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_no2_list, row_cac_no2_count_list))
		o3_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_o3_list, row_cac_o3_count_list))		

if __name__ == '__main__':

	#read file from directory
	for filename in eachFile('./beijing_20170101-20171231'):
		if (re.match(r'.*all.*\.csv', filename)):
			readAddFile(filename)

		if (re.match(r'.*extra.*\.csv', filename)):
			readExtraFile(filename)

	#get IAqi data from day_data
	for day in days_set:
		so2_dict[day] = [cac_aqi.getIAQI(cac_aqi.AIR_TYPE.SO2, x) for x in so2_dict[day]]
		no2_dict[day] = [cac_aqi.getIAQI(cac_aqi.AIR_TYPE.NO2, x) for x in no2_dict[day]]
		pm10_dict[day] = [cac_aqi.getIAQI(cac_aqi.AIR_TYPE.PM10, x) for x in pm10_dict[day]]
		o3_dict[day] = [cac_aqi.getIAQI(cac_aqi.AIR_TYPE.O3, x) for x in o3_dict[day]]
		pm25_dict[day] = [cac_aqi.getIAQI(cac_aqi.AIR_TYPE.PM25, x) for x in pm25_dict[day]]


	#days_set is no order, so we must use list, but now the valiue is string
	days_list = list(days_set)
	days_list.sort()   

	#save Sum AQI Value include every day
	
	aqi_sum_list = [0]*COL_NUM
	aqi_count_list = [0]*COL_NUM
	aqi_avg_list = [0]*COL_NUM

	for day in days_list:
		#Now get the avarage Month AQI
		#the days_list is ordered, but the cell is String
		for index, aqi in enumerate(aqi_dict[day]):
			if aqi>0:
				aqi_sum_list[index] += aqi
				aqi_count_list[index] +=1

	aqi_avg_list = list(map(lambda x,y: round(x/y) if y>0 else 0, aqi_sum_list ,aqi_count_list))
	print(aqi_avg_list)


	################################   Draw Line   ###########################
	plt.figure(num=1, figsize=(14, 6))

	#Draw Rectangle
	dept_list = DEPT_STR.split(',')
	MONTH_COUNT = COL_NUM
	row = [x+1 for x in range(MONTH_COUNT)]
	max_api_value = max(aqi_avg_list)
	slabel = '绿色：优' + '  黄色：良\n' + '棕色：轻度污染\n' + '红色：中度污染' 
	plt.fill_between(row, [50]*MONTH_COUNT, [0]*MONTH_COUNT, facecolor='lime', alpha=1)
	plt.fill_between(row, [100]*MONTH_COUNT, [50]*MONTH_COUNT, facecolor='yellow', alpha=1)
	plt.fill_between(row, [150]*MONTH_COUNT, [100]*MONTH_COUNT, facecolor='sandybrown', alpha=1)
	plt.fill_between(row, [200]*MONTH_COUNT, [150]*MONTH_COUNT, facecolor='red', alpha=1)
	if max_api_value>200:
		slabel = slabel + '\n紫红色：重度污染'
		plt.fill_between(row, [300]*MONTH_COUNT, [200]*MONTH_COUNT, facecolor='fuchsia', alpha=1)
	if max_api_value>300:
		slabel = slabel +  '\n黑红色：严重污染'
		plt.fill_between(row, [500]*MONTH_COUNT, [300]*MONTH_COUNT, facecolor='darkred', alpha=1)

	plt.bar([x+1 for x in range(35)], aqi_avg_list, label = None)
	plt.legend(loc='upper left')
#	plt.grid(True)
	plt.title(INPUT_MONTH[0:4] + "年" + "北京市35个监测点平均AQI指数统计图", fontsize=24)
	for index, day in enumerate([x+1 for x in range(35)]):
		plt.text(day, aqi_avg_list[index], aqi_avg_list[index])
		plt.text(day, 40, dept_list[index], rotation=90, color='white')
	plt.xticks([x+1 for x in range(35)])
	plt.savefig(INPUT_MONTH + '北京市AQI.png', bbox_inches='tight')
	plt.show()
	plt.close()

