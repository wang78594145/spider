# import time
import socket
# # ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
# # print(ptime)
# # print(time.localtime(time.time()))
# #
# # dt = '2018-01-01 10:40:30'
# # input_date = '2019-01-01'
# # order_time = input_date+' 13:30:00'
# # print(order_time)
# # ts = int(time.mktime(time.strptime(order_time, "%Y-%m-%d %H:%M:%S")))
# # ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
# # print(ts)
# # print(int(time.time()))
# # print(ptime)
# def  check_order_date( input_date):
#     "检验输入的日期是否满足30天内的时间范围"
#     #order_time:预约起始时间
#     time_dict={}
#     order_time = input_date+' 13:30:00'
#     #将预约时间换成秒，方便后面进行预约时间范围判断
#     order_time_timestamp = int(time.mktime(time.strptime(order_time, "%Y-%m-%d %H:%M:%S")))
#     #当前时间的时间戳
#     now_time_timestamp = int(time.time())
#     diff_time = order_time_timestamp - now_time_timestamp;
#     if(diff_time<0 or diff_time>90*24*60*60):
#         print("输入的预约租车时间应该在当前日期后90天内,按照默认明天13:30:00作为预约时间")
#         return False
#     time_dict.update(ptime=order_time)
#     #ptime2 格式
#     ptime2 = input_date.replace('-','/')+' 13:30:00'
#     time_dict.update(ptime2=ptime2)
#     dtime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(order_time_timestamp + 24 * 60 * 60 * 3))
#     dtime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(order_time_timestamp + 24 * 60 * 60 * 3))
#     time_dict.update(dtime=dtime)
#     time_dict.update(dtime2=dtime2)
#     return time_dict
#
#
# str = input("输入预约租车时间（格式：2019-01-01）: ");
# check_result = check_order_date(str)
# if check_result == False:
#     # 公共请求参数,借车还车一个城市,一天的价格
#     ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
#     # 用于租车请求格式比当前日期提前一天比如今天2019/9/25 1:00:00 ，则租车日期为2019/9/26 1:30:00
#     ptime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
#     dtime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
#     # 用于还车时间请求格式，比借车时间多两天时间
#     dtime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
# else:
#     # 公共请求参数,借车还车一个城市,一天的价格
#     ptime = check_result['ptime']
#     # 用于租车请求格式比当前日期提前一天比如今天2019/9/25 1:00:00 ，则租车日期为2019/9/26 1:30:00
#     ptime2 = check_result['ptime2']
#     dtime = check_result['dtime']
#     # 用于还车时间请求格式，比借车时间多两天时间
#     dtime2 = check_result['dtime2']
# print(ptime,ptime2,dtime,dtime2)
# proxies={"http": "http://" + "192.168.4.132", "https": "https://" + "192.168.4.132"}
# ip = proxies["http"].replace("http://","")
# print(ip)
# myname = socket.getfqdn(socket.gethostname())
# myaddr = socket.gethostbyname(myname)
# print(myaddr)