#! /usr/bin/env python
#-*-coding:utf-8-*-  
# modify INPUT_MONTH PARAM

#Author : Jackie & Amy
#Date : 2018-01-28

import os
import re
import csv
import math
import matplotlib.pyplot as plt
from pylab import mpl

#input MONTH
INPUT_MONTH = '201712'
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#readData col number
DEPT_STR = '东四,天坛,官园,万寿西宫,奥体中心,农展馆,万柳,北部新区,植物园,丰台花园,云岗,古城,房山,大兴,亦庄,通州,顺义,昌平,门头沟,平谷,怀柔,密云,延庆,定陵,八达岭,密云水库,东高村,永乐店,榆垡,琉璃河,前门,永定门内,西直门北,南三环,东四环'
COL_NUM = 35
# save the days
days_list = []

#save PM_data for the month
pm25_dict = {}
aqi_dict = pm25_dict.copy()
pm25_count = pm25_dict.copy()
aqi_count = pm25_dict.copy()

filename = 'beijing_all_20170108.csv'

def eachFile(filepath):
	patternxml = r'.*all.*' + INPUT_MONTH + '.*\.csv'
	#pathDir =  os.listdir(filepath)
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

def readFile(filename): 
	global pm25_dict, aqi_dict, pm25_count, aqi_count
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		header_row = next(reader)

		#if len is short then the file is not valid
		if len(header_row) != COL_NUM + 3:
			return False
		
		#save indeed row real data
		row_cac_pm25_count_list = [0 for x in range(0, COL_NUM)]
		row_cac_aqi_count_list = row_cac_pm25_count_list[:]
		#save indeed pm25 data
		sum_pm25_list = row_cac_pm25_count_list[:]
		sum_aqi_list = row_cac_pm25_count_list[:]

		# read data from every_row
		for row in reader:
			if len(row) > 10:   # this sentance is not sure
				day = row[0][6:8]  #cut the day
				#read PM2.5
				if row[2] == 'PM2.5':
					for i in range(COL_NUM):
						if is_number(row[i+3]):
							sum_pm25_list[i] += int(row[i+3])
							row_cac_pm25_count_list[i] +=1

				#read AQI
				if row[2] == 'AQI':
					for i in range(COL_NUM):
						if is_number(row[i+3]):
							sum_aqi_list[i] += int(row[i+3])
							row_cac_aqi_count_list[i] +=1
				
		days_list.append(day)
		pm25_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_pm25_list, row_cac_pm25_count_list))
		aqi_dict[day] = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_aqi_list, row_cac_aqi_count_list))


if __name__ == '__main__':
	wanliu_pm_list = []
	wanliu_aqi_list = []
	for file in eachFile('./beijing_20170101-20171231'):
		readFile(file)


	#when readed from file, then pm25_dict{} saved sum_data of each month
	#the aqi_dict{} same to 
	days_list.sort()
	for day in days_list:
		wanliu_pm_list.append(pm25_dict[day][6])
		wanliu_aqi_list.append(aqi_dict[day][6])


	#now pm25_dict{} saved the last average data order by Month
	fig = plt.figure(dpi=128, figsize=(10, 6))
	plt.plot(days_list, wanliu_pm_list, c='red')
	plt.plot(days_list, wanliu_aqi_list, c='blue')
	plt.grid(True)
	#设置图形的格式
	plt.title(INPUT_MONTH[0:4] + "年" + INPUT_MONTH[4:6] + "月万柳地区PM2.5 & AQI 统计图", fontsize=24)
	plt.xlabel('蓝色曲线为AQI,红色曲线为PM2.5', fontsize=16)
#	plt.ylabel("数值", fontsize=16)
	plt.tick_params(axis='both', which='major', labelsize=16)

	#max value
	m_index = wanliu_pm_list.index(max(wanliu_pm_list))
	plt.text(days_list[m_index], wanliu_pm_list[m_index], wanliu_pm_list[m_index])
	#min value
	m_index = wanliu_pm_list.index(min(wanliu_pm_list))
	plt.text(days_list[m_index], wanliu_pm_list[m_index], wanliu_pm_list[m_index])

	#max value
	m_index = wanliu_pm_list.index(max(wanliu_pm_list))
	plt.text(days_list[m_index], wanliu_aqi_list[m_index], wanliu_aqi_list[m_index])

	m_index = wanliu_pm_list.index(min(wanliu_pm_list))
	plt.text(days_list[m_index], wanliu_aqi_list[m_index], wanliu_aqi_list[m_index])

	plt.show()
