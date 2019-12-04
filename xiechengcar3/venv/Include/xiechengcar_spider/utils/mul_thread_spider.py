import requests
import json
import time
import execjs
import random
import os
import csv
from Include.xiechengcar_spider.utils.ipool_utils import excute_main
from Include.xiechengcar_spider.logs.spider_log import Logger

global target_url,log, slog_path, ipool_path,timeout,getCityList,ISDAreaList,searchVehicleList # Logger变量，log输出日志，ip代理池
target_url = "https://www.baidu.com/"#做连接验证
slog_path = os.path.dirname(os.path.dirname(__file__)) + '/logs/spider.log'
log = Logger(slog_path, level='debug')
ipool_path = os.path.dirname(os.path.dirname(__file__)) + '/docs/ip.txt'  # 存放爬取ip的文档path
timeout = (3,10)
# 城市编号
getCityList = "https://m.ctrip.com/restapi/soa2/13617/getCityList"

# 城市下细分城市
ISDAreaList = "https://m.ctrip.com/restapi/soa2/13617/ISDAreaList"

# 借车点车辆细节
searchVehicleList = "https://m.ctrip.com/restapi/soa2/13617/searchVehicleList"


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


def checkip(target_url, ip, retries):
    "检查获取到的ip是否可用"
    headers = get_agent()  # 定制请求头
    proxies2 = {"http": "http://" + ip, "https": "http://" + ip}  # 代理ip
    try:
        response = requests.get(url=target_url, proxies=proxies2, headers=headers, timeout=timeout).status_code
        if response == 200:
            log.logger.debug("check" + ip + "可用，返回true")
            return True
        else:
            for i in range(retries):
                log.logger.warning("response 不等于200，重连" + str(retries) + "次，尝试重连次数：" + str(i + 1))
                if checkip(target_url, ip, 0):
                    return True
                continue
            log.logger.debug("check" + ip + "不可用返回false")
            return False
    except:
        for i in range(retries):
            log.logger.warning("request抛出异常，重连" + str(retries) + "次，尝试重连次数：" + str(i + 1))
            # log.debug("Let me sleep for 3 seconds")
            # log.debug("ZZzzzz...")
            time.sleep(3)
            # log.debug("Was a nice sleep, now let me continue...")
            if checkip(target_url, ip, 0):
                return True
            continue
        log.logger.debug("check" + ip + "连接失败，处理异常返回false")
        return False


def get_proxies(target_url, ip_list):
    # log = Logger('spider.log', level='debug')
    "从ip代理池里筛选一个可用的代理ip"
    ip = random.choice(ip_list)
    if checkip(target_url, ip, 3):
        proxies = {"http": "http://" + ip, "https": "https://" + ip}  # 代理ip
        return proxies
    else:
        log.logger.debug("移除此代理ip" + ip + "，换新代理，连接池剩余代理数量为" + str(len(ip_list)))
        ip_list.remove(ip)
        if len(ip_list) > 0:
            get_proxies(target_url, ip_list)
        else:
            log.logger.warning("代理池所有ip都不可用，正在更新代理池")
            excute_main(ipool_path)
            ip_list = get_ip_pool(ip_list)
            get_proxies(target_url, ip_list)


def get_ip_pool(list):
    "获取ip代理池"
    f = open(ipool_path, "r")
    for line in f.readlines():
        if len(line.strip()) != 0:
            list.append(line)
    f.close()
    return list


# print(get_avail_proxies())
def get_sign(ptime2, dtime2, pcid, dcid):
    "解携程searchVehicleList 传入参数sign；此方法调用nodejs函数，需要安装nodejs"
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
    " 转成json并以payload方式获取post请求的url返回的字典值，并取出需要的key标签对应的listvalue值，转换成json格式进行解析"
    list = requests.post(post_url, data=json.dumps(post_payload), headers=header).content.decode("utf-8")
    return json.loads(list)[dict_target]


def deal_conn_exception(post_url, payload, header, proxies,ip_list):
    "处理ip代理连接异常,连接尝试30次，如果成功，直接返回list内容，如果失败，更换ip再获取可用ip返回list结果集"
    # log = Logger('spider.log', level='debug')
    for i in range(10):
        log.logger.warning("连接尝试次数：" + str(i + 1))
        try:
            list = json.loads(
                requests.post(post_url, data=json.dumps(payload),
                              headers=header, proxies=proxies, timeout=timeout).content.decode(
                    "utf-8")
            )
            log.logger.debug("重新连接成功，跳出重连接")
            return list
        except:
            log.logger.warning("Connection refused by the server,sleep for 3 seconds..")
            # print("Let me sleep for 3 seconds")
            # print("ZZzzzz...")
            time.sleep(3)
            # print("Was a nice sleep, now let me continue...")
            if i >= 9:
                log.logger.debug("准备更换当前代理Ip")
                proxies = get_proxies(target_url, ip_list)
                try:
                    list = json.loads(
                        requests.post(ISDAreaList, data=json.dumps(area_list_payload), proxies=proxies, headers=header,
                                      timeout=timeout).content.decode("utf-8"))
                    return list
                except:
                    # 递归处理post抛出来的异常，直到返回当前查询数据为止，否则会丢数据或者程序退出。
                    area_list = deal_conn_exception(ISDAreaList, area_list_payload, header, proxies,ip_list)
                # list = json.loads(
                #     requests.post(post_url, data=json.dumps(payload),
                #                   headers=header, proxies=proxies,timeout=(3)).content.decode(
                #         "utf-8")
                # )


def get_citylist_payload():
    "构造CityList的payload数据"
    return {
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


def get_arealist_payload(f_id):
    "构造arealist的 payload数据"
    return {
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


def get_vehiclelist_payload(channelid, ptime2, dtime2, paddr, plat, plng, dcid, dcname, sign):
    "构造ehiclelist的payload"
    return {
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


def get_random_header():
    "得到随机的header"
    random_agent = get_agent()['User-Agent']
    return {
        # payload请求设置类型json，约定返回值也为json
        'Content-Type': 'application/json',
        'Accept': 'application/json',

        # 如网站有Referer反爬，可以设置简单反爬
        'Sec-Fetch-Mode': 'cors',
        'Origin': 'https://car.ctrip.com',
        'Referer': 'https://car.ctrip.com/zuche/index',
        'User-Agent': random_agent
    }


def del_exist_file(file_path):
    "判断文件是否存在,如果存在删掉"
    # os.path.exists(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        log.logger.warning("正在删除已经存在的路径文件：" + file_path)


def write_csv(csv_path, info_list):
    "将结果保存到csv中"
    # encoding='utf-8-sig为了解决在windos端有乱码尔pycharm上没有
    with open(csv_path, "a", newline="", encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)  # csv.writer
        csv_writer.writerow(info_list)
        csv_file.close()


def spidier_start(csv_path):
    "开始执行携程用车全国数据爬取方法"
    # log = Logger('spider.log', level='debug')
    # log = Logger('spider.log',level = 'debug')
    ip_list = []
    log.logger.debug("target_url:" + target_url)
    ip_list = get_ip_pool(ip_list)
    proxies = get_proxies(target_url, ip_list)
    # 定义随机header
    header = get_random_header()

    # # 城市编号
    # getCityList = "https://m.ctrip.com/restapi/soa2/13617/getCityList"
    #
    # # 城市下细分城市
    # ISDAreaList = "https://m.ctrip.com/restapi/soa2/13617/ISDAreaList"
    #
    # # 借车点车辆细节
    # searchVehicleList = "https://m.ctrip.com/restapi/soa2/13617/searchVehicleList"

    # 公共请求参数,借车还车一个城市,一天的价格
    ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
    # 用于租车请求格式比当前日期提前一天比如今天2019/9/25 1:00:00 ，则租车日期为2019/9/26 1:30:00
    ptime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
    dtime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
    # 用于还车时间请求格式，比借车时间多两天时间
    dtime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
    # CityList的payload数据
    city_list_payload = get_citylist_payload()

    # 获取CityListpost返回的信息，因为每次启动只有一次访问，基本不会出问题，就不做ip连接异常处理
    city_list = requests.post(getCityList, data=json.dumps(city_list_payload), headers=header).content.decode("utf-8")

    # 程序开始先删除已经存在的冲突文件，然后写入csv头标签
    # csv_path = "car_spider.csv"
    del_exist_file(csv_path)
    write_csv(csv_path, ["f_id", "f_name", "paddr", "bname", "vname",
                         "trans", "vtype", "low_price", "renter1", "price1",
                         "renter2", "price2", "renter3", "price3"])
    # 获取pcity_list返回的json信息。
    j_pcity_list = json.loads(city_list)["pcitylist"]
    # 此处需要遍历j_pcity_list，作为测试先获取第一个城市id
    # f_id = j_pcity_list[0]["id"]
    # f_name = j_pcity_list[0]["name"]
    for city in j_pcity_list:
        # 租车城市id
        f_id = str(city["id"])
        # 组成城市id对应的城市名称
        f_name = city["name"]
        current_timestamp = time.time()
        # 构造area payload
        area_list_payload = get_arealist_payload(f_id)

        # 获取area_list
        try:
            area_list = json.loads(
                requests.post(ISDAreaList, data=json.dumps(area_list_payload), proxies=proxies, headers=header,
                              timeout=timeout).content.decode("utf-8"))
        except:
            area_list = deal_conn_exception(ISDAreaList, area_list_payload, header, proxies,ip_list)

        # 判断请求是否完整
        if (area_list["responseStatus"]["Ack"] == "Success"):
            # log.info("数据获取成功··")
            log.logger.debug("开始构造租车站点url··")
            # 获取alist
            alist = area_list["alist"]
            pcid = f_id
            dcid = f_id
            pcname = f_name
            dcname = f_name
            for area in alist:
                # -----------------------构造租车页面url-----------------------
                # 定义随机header
                vehicle_header = get_random_header()
                # 获取alist中的list
                llist = area["llist"]
                for lllist in llist:
                    # 取车点
                    paddr = lllist["lname"]
                    # 取车点经纬度
                    plat = lllist["lat"]
                    plng = lllist["lng"]
                    # 还车点
                    daddr = lllist["lname"]
                    # 还车点经纬度
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
                    # 解码携程sign加密
                    sign = get_sign(ptime2, dtime2, pcid, dcid)
                    #   print(sign)
                    # 构造searchVehicleList_payload
                    vehicle_list_payload = get_vehiclelist_payload(channelid, ptime2, dtime2, paddr, plat, plng, dcid,
                                                                   dcname, sign)
                    # 每次新的站点都随机一个新ip解决连接次数过多问题
                    proxies = get_proxies(target_url, ip_list)
                    try:
                        vehicle_list = json.loads(
                            requests.post(searchVehicleList, data=json.dumps(vehicle_list_payload),
                                          headers=vehicle_header, proxies=proxies, timeout=timeout).content.decode(
                                "utf-8")
                        )
                        # print(vehicle_list)
                    except:
                        log.logger.warning("连接被拒绝，准备重试")
                        vehicle_list = deal_conn_exception(searchVehicleList, vehicle_list_payload, vehicle_header,
                                                           proxies,ip_list)
                    # 判断请求是否完整
                    if (vehicle_list["responseStatus"]["Ack"] == "Success"):
                        log.logger.info(pcname + ":" + paddr + "租车信息获取成功")
                        carinfo_list = vehicle_list["plist"]
                        for car_info in carinfo_list:
                            # 定义一个list用于存储用车信息
                            info_list = []
                            info_list.append(f_id)
                            info_list.append(f_name)
                            info_list.append(paddr)
                            # 车品牌
                            bname = car_info["bname"]
                            info_list.append(bname)
                            # 车具体型号
                            vname = car_info["vname"]
                            info_list.append(vname)
                            # 自动挡或者手动挡
                            trans = car_info["trans"]
                            info_list.append(trans)
                            # 车所属类型：vtype 2:经济型  3：舒适性  4：商务 5：豪华型 6：SUV 7:小巴士 9：跑车  11：房车
                            vtype = car_info["vtype"]
                            info_list.append(vtype)
                            low_price = car_info["price"]
                            info_list.append(low_price)
                            # 车座
                            seat = car_info["seat"]
                            # 排量
                            displace = car_info["displace"]
                            # 附近租车热点排名
                            hotSort = car_info["hotSort"]
                            # 不获取同租车公司不同报价列表
                            leases_plist = car_info["slist"]
                            for lease_info in leases_plist:
                                # 出租商
                                lease_company = lease_info["cyvname"]
                                info_list.append(lease_company)
                                # 当前租赁单价
                                lease_price = lease_info["cprice"]
                                info_list.append(lease_price)
                                # 出租商距离
                                # lease1_distance = lease_info["diststr"]
                                write_csv(csv_path, info_list)
                            # log.info(
                            #     "租赁地点：" + pcname + "_" + paddr + "\t车品牌："
                            #     + bname + "\t车型号："
                            #     + vname + "\t自动挡或者手动挡：" + trans + " \t车座:" + str(seat))
        else:
            log.logger.error("检查payload请求数据是否准确···,程序退出")
    log.logger.info("全国用车数据爬取结束")


#--------------------------------------------主函数运行-----------------------------------------------------------------

if __name__ == '__main__':
    ip_list = []
    target_url = "https://www.baidu.com/"
    ip_list = get_ip_pool(ip_list)
    proxies = get_proxies(target_url, ip_list)
    # 定义随机header
    header = get_random_header()

    # # 城市编号
    # getCityList = "https://m.ctrip.com/restapi/soa2/13617/getCityList"
    #
    # # 城市下细分城市
    # ISDAreaList = "https://m.ctrip.com/restapi/soa2/13617/ISDAreaList"
    #
    # # 借车点车辆细节
    # searchVehicleList = "https://m.ctrip.com/restapi/soa2/13617/searchVehicleList"

    # 公共请求参数,借车还车一个城市,一天的价格
    ptime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
    # 用于租车请求格式比当前日期提前一天比如今天2019/9/25 1:00:00 ，则租车日期为2019/9/26 1:30:00
    ptime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
    dtime = time.strftime('%Y-%m-%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
    # 用于还车时间请求格式，比借车时间多两天时间
    dtime2 = time.strftime('%Y/%m/%d 13:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
    # CityList的payload数据
    city_list_payload = get_citylist_payload()

    # 获取CityListpost返回的信息，因为每次启动只有一次访问，基本不会出问题，就不做ip连接异常处理
    city_list = requests.post(getCityList, data=json.dumps(city_list_payload), headers=header).content.decode("utf-8")

    # 程序开始先删除已经存在的冲突文件，然后写入csv头标签
    csv_path = "car_spider.csv"
    del_exist_file(csv_path)
    write_csv(csv_path, ["f_id", "f_name", "paddr", "bname", "vname",
                         "trans", "vtype", "low_price", "renter1", "price1",
                         "renter2", "price2", "renter3", "price3"])
    # 获取pcity_list返回的json信息。
    j_pcity_list = json.loads(city_list)["pcitylist"]
    # 此处需要遍历j_pcity_list，作为测试先获取第一个城市id
    # f_id = j_pcity_list[0]["id"]
    # f_name = j_pcity_list[0]["name"]
    for city in j_pcity_list:
        # 租车城市id
        f_id = str(city["id"])
        # 组成城市id对应的城市名称
        f_name = city["name"]
        current_timestamp = time.time()
        # 构造area payload
        area_list_payload = get_arealist_payload(f_id)

        # 获取area_list
        try:
            area_list = json.loads(
                requests.post(ISDAreaList, data=json.dumps(area_list_payload), proxies=proxies, headers=header,
                              timeout=timeout).content.decode("utf-8"))
        except:
            area_list = deal_conn_exception(ISDAreaList, area_list_payload, header, proxies,ip_list)

        # 判断请求是否完整
        if (area_list["responseStatus"]["Ack"] == "Success"):
            print("数据获取成功··")
            print("开始构造url··")
            # 获取alist
            alist = area_list["alist"]
            pcid = f_id
            dcid = f_id
            pcname = f_name
            dcname = f_name
            for area in alist:
                # -----------------------构造租车页面url-----------------------
                # 定义随机header
                vehicle_header = get_random_header()
                # 获取alist中的list
                llist = area["llist"]
                for lllist in llist:
                    # 取车点
                    paddr = lllist["lname"]
                    # 取车点经纬度
                    plat = lllist["lat"]
                    plng = lllist["lng"]
                    # 还车点
                    daddr = lllist["lname"]
                    # 还车点经纬度
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
                    # 解码携程sign加密
                    sign = get_sign(ptime2, dtime2, pcid, dcid)
                    #   print(sign)
                    # 构造searchVehicleList_payload
                    vehicle_list_payload = get_vehiclelist_payload(channelid, ptime2, dtime2, paddr, plat, plng, dcid,
                                                                   dcname, sign)
                    # 每次新的站点都随机一个新ip解决连接次数过多问题
                    proxies = get_proxies(target_url, ip_list)
                    try:
                        vehicle_list = json.loads(
                            requests.post(searchVehicleList, data=json.dumps(vehicle_list_payload),
                                          headers=vehicle_header, proxies=proxies, timeout=timeout).content.decode(
                                "utf-8")
                        )
                        print(vehicle_list)
                    except:
                        print("连接被拒绝，准备重试")
                        vehicle_list = deal_conn_exception(searchVehicleList, vehicle_list_payload, vehicle_header,
                                                           proxies,ip_list)
                    # 判断请求是否完整
                    if (vehicle_list["responseStatus"]["Ack"] == "Success"):
                        print("车辆信息获取成功")
                        carinfo_list = vehicle_list["plist"]
                        for car_info in carinfo_list:
                            # 定义一个list用于存储用车信息
                            info_list = []
                            info_list.append(f_id)
                            info_list.append(f_name)
                            info_list.append(paddr)
                            # 车品牌
                            bname = car_info["bname"]
                            info_list.append(bname)
                            # 车具体型号
                            vname = car_info["vname"]
                            info_list.append(vname)
                            # 自动挡或者手动挡
                            trans = car_info["trans"]
                            info_list.append(trans)
                            # 车所属类型：vtype 2:经济型  3：舒适性  4：商务 5：豪华型 6：SUV 7:小巴士 9：跑车  11：房车
                            vtype = car_info["vtype"]
                            info_list.append(vtype)
                            low_price = car_info["price"]
                            info_list.append(low_price)
                            # 车座
                            seat = car_info["seat"]
                            # 排量
                            displace = car_info["displace"]
                            # 附近租车热点排名
                            hotSort = car_info["hotSort"]
                            # 不获取同租车公司不同报价列表
                            leases_plist = car_info["slist"]
                            for lease_info in leases_plist:
                                # 出租商
                                lease_company = lease_info["cyvname"]
                                info_list.append(lease_company)
                                # 当前租赁单价
                                lease_price = lease_info["cprice"]
                                info_list.append(lease_price)
                                # 出租商距离
                                # lease1_distance = lease_info["diststr"]
                                write_csv(csv_path, info_list)
                            print(
                                "租赁地点：" + pcname + "_" + paddr + "\t车品牌："
                                + bname + "\t车型号："
                                + vname + "\t自动挡或者手动挡：" + trans + " \t车座:" + str(seat))
        else:
            print("检查请求数据是否准确···")
