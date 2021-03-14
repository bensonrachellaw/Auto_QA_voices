request = "闹钟14点23分"
request_1 = request[2:]
my_hour = request_1.split('点')[0]
my_minute = request_1.split('点')[1].split('分')[0]
print(my_hour)
print(my_minute)