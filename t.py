ls1 = range(0, 10)
ls2 = range(11, 20)

v = list(filter(lambda x:True if x % 3 == 0 else False, range(100))) 
print(v)

v = list(map(lambda x,y:round(x/y) if y>0  else 0, ls2, ls1))
print(v)


		print(avg_pm25_list)
		print(pm25_dict[month])
		print(pm25_count[month])

		print(avg_aqi_list)
		print(aqi_dict[month])
		print(aqi_count[month])

