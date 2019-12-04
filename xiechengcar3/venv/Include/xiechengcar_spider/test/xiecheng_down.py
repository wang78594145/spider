import requests
import json
import time
import execjs
import random


def get_agent():
    "随机获取一个header头的User-Agent"
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    user_agent = random.choice(user_agent_list)
    agent = {'User-Agent': user_agent}
    return agent


def checkip(targeturl, ip):
    "检查获取到的ip是否可用"
    headers = get_agent()  # 定制请求头
    proxies = {"http": "http://" + ip, "https": "http://" + ip}  # 代理ip
    try:
        response = requests.get(url=targeturl, proxies=proxies, headers=headers, timeout=5).status_code
        if response == 200:
            return True
        else:
            return False
    except:
        return False


def get_proxies(target_url, ip_list):
    "获取可用的代理ip"
    ip = random.choice(ip_list)
    if checkip(target_url, ip):
        proxies = {"http": "http://" + ip, "https": "https://" + ip}  # 代理ip
        return proxies
    else:
        ip_list.remove(ip)
        if len(ip_list) > 0:
            get_proxies(target_url, ip_list)
        else:
            return "代理池中所有ip都不可用"


# def get_avail_proxies():
#     "获取最终可用的proxies代理信息"
#     f = open("ip.txt", "r")
#     ip_list = []
#     for line in f.readlines():
#         if len(line.strip()) != 0:
#             ip_list.append(line)
#     #ip = random.choice(ip_list)
#     target_url = "https://www.baidu.com/"
#     return get_proxies(target_url,ip_list)
f = open("ip.txt", "r")
ip_list = []
for line in f.readlines():
    if len(line.strip()) != 0:
        ip_list.append(line)
    # ip = random.choice(ip_list)
f.close()
target_url = "https://www.baidu.com/"
proxies = get_proxies(target_url, ip_list)


# print(get_avail_proxies())
def get_sign(ptime2, dtime2, pcid, dcid):
    "解携程searchVehicleList 传入参数sign"
    ctx = execjs.compile("""
            function cmd5(e,t,n,r){
            const crypto = require('crypto');
            var a = "" + n + t + r +e,
            i = [],
            o = crypto.createCipher('aes-128-ecb', "9102iosd8431ytl9", "");
            return i.push(o.update(a,"utf8","hex")),
            i.push(o.final("hex")),
            crypto.createHash("md5").update(i.join("") + n).digest("hex");
            }
    """)
    return ctx.call("cmd5", ptime2, dtime2, pcid, dcid)


# 获取post的payload的返回信息标签内容
def get_payload(post_url, post_payload, header, dict_target):
    # 转成json并以payload方式获取post请求的url返回的字典值，并取出需要的key标签对应的listvalue值，转换成json格式进行解析
    list = requests.post(post_url, data=json.dumps(city_list_payload), headers=header).content.decode("utf-8")
    return json.loads(list)[dict_target]

#--------------------------------------------主函数运行-----------------------------------------------------------------

if __name__ == '__main__':
    # 定义随机header
    random_agent = get_agent()['User-Agent']
    header = {
        # payload请求设置类型json，约定返回值也为json
        'Content-Type': 'application/json',
        'Accept': 'application/json',

        # 如网站有Referer反爬，可以设置简单反爬
        'Sec-Fetch-Mode': 'cors',
        'Origin': 'https://car.ctrip.com',
        'Referer': 'https://car.ctrip.com/zuche/index',
        'User-Agent': random_agent
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    # 城市编号
    getCityList = "https://m.ctrip.com/restapi/soa2/13617/getCityList"

    # 城市下细分城市
    ISDAreaList = "https://m.ctrip.com/restapi/soa2/13617/ISDAreaList"

    # 借车点车辆细节
    searchVehicleList = "https://m.ctrip.com/restapi/soa2/13617/searchVehicleList"

    # CityList的payload数据
    city_list_payload = {
        # 可以从cookie中获取，默认为0也可以
        "heads": {"serviceFrom": "c_online", "channel": "2", "alliance": {"id": "0", "sid": "0"},
                  "union": {"allianceid": "", "sid": "", "ouid": "", "click_time": "", "click_url": "",
                            "ext_value": ""}},
        "carhead": {"serviceFrom": "c_online", "channel": "2", "alliance": {"id": "0", "sid": "0"},
                    "union": {"allianceid": "", "sid": "", "ouid": "", "click_time": "", "click_url": "",
                              "ext_value": ""}},
        "head": {"cid": "", "ctok": "", "cver": "803.000", "lang": "", "sauth": "", "sid": "0", "syscode": ""},
        "cVer": "19.07.22",
        "isfullinfo": 0
    }

    # 获取CityList
    # city_list = requests.post(getCityList, data=json.dumps(city_list_payload), headers=header).content.decode("utf-8")

    # # 转成json并获取pcitylist
    # j_pcity_list = get_payload(getCityList,city_list_payload,header,"pcitylist")

    # 获取CityListpost返回的信息
    city_list = requests.post(getCityList, data=json.dumps(city_list_payload), headers=header).content.decode("utf-8")
    # 转成json并获取pcitylist信息
    j_pcity_list = json.loads(city_list)["pcitylist"]

    # 此处需要遍历j_pcity_list，作为测试先获取第一个城市id
    # f_id = j_pcity_list[0]["id"]
    # f_name = j_pcity_list[0]["name"]
    for city in j_pcity_list:
        # 租车城市id
        # f_id = str(j_pcity_list[0]["id"])
        f_id = str(city["id"])
        # 组成城市id对应的城市名称
        # f_name = j_pcity_list[0]["name"]
        f_name = city["name"]
        current_timestamp = time.time()
        # 构造area payload
        area_list_payload = {
            "heads": {"serviceFrom": "c_online", "channel": "2", "alliance": {"id": "0", "sid": "0"},
                      "union": {"allianceid": "", "sid": "", "ouid": "", "click_time": "", "click_url": "",
                                "ext_value": ""}},
            "carhead": {"serviceFrom": "c_online", "channel": "2", "alliance": {"id": "0", "sid": "0"},
                        "union": {"allianceid": "", "sid": "", "ouid": "", "click_time": "", "click_url": "",
                                  "ext_value": ""}},
            "head": {"cid": "", "ctok": "", "cver": "803.000", "lang": "", "sauth": "", "sid": "0", "syscode": ""},
            "cVer": "19.07.22",
            "cid": f_id
        }

        # 获取area_list
        area_list = json.loads(
            requests.post(ISDAreaList, data=json.dumps(area_list_payload), headers=header).content.decode("utf-8"))
        # 判断请求是否完整
        if (area_list["responseStatus"]["Ack"] == "Success"):
            print("数据获取成功··")
            print("开始构造url··")
            # 获取alist
            alist = area_list["alist"]

            # 公共请求参数,借车还车一个城市,一天的价格
            ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
            # 用于租车请求格式比当前日期提前一天比如今天2019/9/25 1:00:00 ，则租车日期为2019/9/26 1:30:00
            ptime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
            dtime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
            # 用于还车时间请求格式，比借车时间多两天时间
            dtime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
            pcid = f_id
            dcid = f_id
            pcname = f_name
            dcname = f_name
            for area in alist:
                # 构造租车页面url

                # 获取alist中的list
                llist = area["llist"]
                for lllist in llist:
                    paddr = lllist["lname"]
                    plat = lllist["lat"]
                    plng = lllist["lng"]
                    daddr = lllist["lname"]
                    dlat = lllist["lat"]
                    dlng = lllist["lng"]

                    # 没什么用可以直接给默认
                    uid = 0
                    channelid = 2

                    result_url = "https://car.ctrip.com/zuche/list?&ptime=" + \
                                 ptime + "&pcid=" + pcid + "&pcname=" + \
                                 pcname + "&paddr=" + paddr + "&plat=" + \
                                 plat + "&plng=" + plng + "&dtime=" + \
                                 dtime + "&dcid=" + dcid + "&dcname=" + dcname + "&daddr=" + daddr + "&dlat=" + dlat + "&dlng=" + dlng + "&uid=" + str(
                        uid) + "&channelid=" + str(channelid)
                    # print(result_url)

                    sign = get_sign(ptime2, dtime2, pcid, dcid)
                    #   print(sign)
                    # 构造searchVehicleList_payload
                    vehicle_list_payload = {
                        "heads": {"serviceFrom": "c_online", "channel": channelid, "alliance": {"id": "0", "sid": "0"},
                                  "union": {}},
                        "carhead": {"serviceFrom": "c_online", "channel": channelid,
                                    "alliance": {"id": "0", "sid": "0"},
                                    "union": {}},
                        "head": {"cid": "", "ctok": "", "cver": "", "lang": "", "sauth": "", "sid": "0", "syscode": ""},
                        "cVer": "19.07.22", "ptime": ptime2, "rtime": dtime2,
                        "pinfo": {"addr": paddr, "lat": plat, "lng": plng, "cid": dcid, "cname": dcname},
                        "rinfo": {"addr": paddr, "lat": plat, "lng": plng, "cid": dcid, "cname": dcname},
                        "userGrade": 0, "channel": 2, "areatype": 0, "sf": "c_pc", "pickupondoor": 0,
                        "pickoffondoor": 0,
                        "vid": "",
                        "wlver": "", "sign": sign
                    }
                    vehicle_header = {
                        # payload请求设置类型json，约定返回值也为json
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',

                        # 如网站有Referer反爬，可以设置简单反爬
                        'Sec-Fetch-Mode': 'cors',
                        'Origin': 'https://car.ctrip.com',
                        'Referer': "https://car.ctrip.com/zuche/list?&ptime=2019-09-24%2010:00&pcid=2&pcname=%E4%B8%8A%E6%B5%B7&paddr=%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BAT2%E8%88%AA%E7%AB%99%E6%A5%BC&plat=31.193274&plng=121.326276&dtime=2019-09-26%2010:00&dcid=2&dcname=%E4%B8%8A%E6%B5%B7&daddr=%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BAT2%E8%88%AA%E7%AB%99%E6%A5%BC&dlat=31.193274&dlng=121.326276&uid=0&channelid=2",
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                    }
                    # 每次新的站点都随机一个新ip解决连接次数过多问题
                    proxies = get_proxies(target_url, ip_list)
                    try:
                        vehicle_list = json.loads(
                            requests.post(searchVehicleList, data=json.dumps(vehicle_list_payload),
                                          headers=header, proxies=proxies).content.decode(
                                "utf-8")
                        )
                        print(vehicle_list)
                    except:
                        print("连接被拒绝，准备重试")
                        for i in range(30):
                            print("连接尝试次数：" + str(i))
                            try:
                                vehicle_list = json.loads(
                                    requests.post(searchVehicleList, data=json.dumps(vehicle_list_payload),
                                                  headers=header, proxies=proxies).content.decode(
                                        "utf-8")
                                )
                                print("重新连接成功，跳出重连接")
                                break
                            except:
                                print("Connection refused by the server..")
                                print("Let me sleep for 5 seconds")
                                print("ZZzzzz...")
                                time.sleep(5)
                                print("Was a nice sleep, now let me continue...")
                                if i < 30:
                                    continue
                                else:
                                    print("准备更换代理Ip")
                                    ip_list.remove(ip)
                                    proxies = get_proxies(target_url, ip_list)
                                    vehicle_list = json.loads(
                                        requests.post(searchVehicleList, data=json.dumps(vehicle_list_payload),
                                                      headers=header, proxies=proxies).content.decode(
                                            "utf-8")
                                    )

                    # 判断请求是否完整
                    if (vehicle_list["responseStatus"]["Ack"] == "Success"):
                        print("车辆信息获取成功")
                        carinfo_list = vehicle_list["plist"]
                        for car_info in carinfo_list:
                            # 最低价
                            low_price = car_info["price"]
                            # 车品牌
                            bname = car_info["bname"]
                            # 车具体型号
                            vname = car_info["vname"]
                            # 自动挡或者手动挡
                            trans = car_info["trans"]
                            # 车座
                            seat = car_info["seat"]
                            # 排量
                            displace = car_info["displace"]
                            hotSort = car_info["hotSort"]
                            leases_plist = car_info["slist"]
                            list = []
                            for lease_info in leases_plist:
                                # 当前租赁单价
                                lease1_price = lease_info["cprice"]
                                # 出租商
                                lease1_company = lease_info["cyvname"]
                                # 出租商距离
                                # lease1_distance = lease_info["diststr"]
                                info = lease1_company + "_" + str(lease1_price)
                                list.append(info)

                            print(
                                "租赁地点：" + pcname + "_" + paddr + "\t车品牌：" + bname + "\t车型号：" + vname + "\t自动挡或者手动挡：" + trans + "\t车座" +str(seat)+ "\t租赁商：" + str(
                                    list))


        else:
            print("检查请求数据是否准确···")
