#! /usr/bin/env python
#-*-coding:utf-8-*-  

#Author : Jackie & Amy
#Date : 2018-01-28

import os
import re
import csv
import math
import matplotlib.pyplot as plt

#readData col number
DEPT_STR = '东四,天坛,官园,万寿西宫,奥体中心,农展馆,万柳,北部新区,植物园,丰台花园,云岗,古城,房山,大兴,亦庄,通州,顺义,昌平,门头沟,平谷,怀柔,密云,延庆,定陵,八达岭,密云水库,东高村,永乐店,榆垡,琉璃河,前门,永定门内,西直门北,南三环,东四环'
COL_NUM = 35

STR_MONTH_DICT = {
	'01': '一月',
	'02': '二月',
	'03': '三月',
	'04': '四月',
	'05': '五月',
	'06': '六月',
	'07': '七月',
	'08': '八月',
	'09': '九月',
	'10': '十月',
	'11': '十一月',
	'12': '十二月'
}
#save PM_data for the month
pm25_dict = {
	'01':[0 for x in range(COL_NUM)],
	'02':[0 for x in range(COL_NUM)],
	'03':[0 for x in range(COL_NUM)],
	'04':[0 for x in range(COL_NUM)],
	'05':[0 for x in range(COL_NUM)],
	'06':[0 for x in range(COL_NUM)],
	'07':[0 for x in range(COL_NUM)],
	'08':[0 for x in range(COL_NUM)],
	'09':[0 for x in range(COL_NUM)],
	'10':[0 for x in range(COL_NUM)],
	'11':[0 for x in range(COL_NUM)],
	'12':[0 for x in range(COL_NUM)]
}
aqi_dict = pm25_dict.copy()
pm25_count = pm25_dict.copy()
aqi_count = pm25_dict.copy()

filename = 'beijing_all_20170108.csv'

def eachFile(filepath):
	patternxml = r'.*all.*\.csv'
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
				month = row[0][4:6]
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
				
		avg_pm25_list = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_pm25_list, row_cac_pm25_count_list))
		avg_aqi_list = list(map(lambda x,y: round(x/y) if y>0 else 0, sum_aqi_list, row_cac_aqi_count_list))

		pm25_dict[month] = list(map(lambda x,y: x+y, pm25_dict[month], avg_pm25_list))
		pm25_count[month] = list(map(lambda x,y: x+1 if y>0 else x,  pm25_count[month], avg_pm25_list))

		aqi_dict[month] = list(map(lambda x,y: x+y, aqi_dict[month], avg_aqi_list))
		aqi_count[month] = list(map(lambda x,y: x+1 if y>0 else x,  aqi_count[month], avg_aqi_list))


if __name__ == '__main__':
	wanliu_pm_list = []
	wanliu_aqi_list = []
	for file in eachFile('./beijing_20170101-20171231'):
		readFile(file)


	#when readed from file, then pm25_dict{} saved sum_data of each month
	#the aqi_dict{} same to 

	month_list = list(STR_MONTH_DICT.keys())
	for key in month_list:
		pm25_dict[key] = list(map(lambda x,y: round(x/y) if y>0 else 0, pm25_dict[key], pm25_count[key]))
		aqi_dict[key] = list(map(lambda x,y: round(x/y) if y>0 else 0, aqi_dict[key], aqi_count[key]))
		wanliu_pm_list.append(pm25_dict[key][6])
		wanliu_aqi_list.append(aqi_dict[key][6])


	print(wanliu_pm_list)
	#now pm25_dict{} saved the last average data order by Month
	fig = plt.figure(dpi=128, figsize=(10, 6))
	plt.plot(month_list, wanliu_pm_list, c='red')
	plt.plot(month_list, wanliu_aqi_list, c='blue')
	#设置图形的格式
	plt.title("2017 WanLiu PM2.5 Value", fontsize=24)
	plt.xlabel('Month', fontsize=16)
	plt.ylabel("Value", fontsize=16)
	plt.tick_params(axis='both', which='major', labelsize=16)
	plt.show()
 