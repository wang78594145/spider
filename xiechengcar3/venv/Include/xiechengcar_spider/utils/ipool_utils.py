#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests,threading,datetime
from bs4 import BeautifulSoup
import random
import os
import socket
from Include.xiechengcar_spider.logs.spider_log import Logger
"""
1、抓取西刺代理网站的代理ip
2、并根据指定的目标url,对抓取到ip的有效性进行验证
3、最后存到指定的path
"""
global log,ilog_path
ilog_path = os.path.dirname(os.path.dirname(__file__)) + '/docs/ipool.log'
log = Logger(ilog_path, level='info')
# ------------------------------------------------------文档处理--------------------------------------------------------
# 写入文档
def write(path,text):
    with open(path,'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
        f.close()
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
        f.close()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt
# ----------------------------------------------------------------------------------------------------------------------
# 计算时间差,格式: 时分秒
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
# ----------------------------------------------------------------------------------------------------------------------
# 返回一个随机的请求头 headers
def getheaders():
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
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers
# -----------------------------------------------------检查ip是否可用----------------------------------------------------
def checkip(targeturl,ip):
    headers =getheaders()  # 定制请求头
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    try:
        response=requests.get(url=targeturl,proxies=proxies,headers=headers,timeout=(3,5)).status_code
        if response == 200 :
            return True
        else:
            return False
    except:
        return False

#-------------------------------------------------------获取代理方法----------------------------------------------------
# 免费代理 XiciDaili
def findip(type,pagenum,targeturl,path): # ip类型,页码,目标url,存放ip的路径
    list={'1': 'http://www.xicidaili.com/nt/', # xicidaili国内普通代理
          '2': 'http://www.xicidaili.com/nn/', # xicidaili国内高匿代理
          '3': 'http://www.xicidaili.com/wn/', # xicidaili国内https代理
          '4': 'http://www.xicidaili.com/wt/'} # xicidaili国外http代理
    url=list[str(type)]+str(pagenum) # 配置url
    ip = [];
    ips = get_ip_pool(ip)
    if ips:
        proxiess = get_proxies(targeturl, ips)
        headers = getheaders() # 定制请求头
        html=requests.get(url=url,proxies=proxiess,headers=headers,timeout = (3,5)).text
    headers = getheaders()  # 定制请求头
    html = requests.get(url=url, headers=headers, timeout=(3, 5)).text
    soup=BeautifulSoup(html,'lxml')
    # soup = BeautifulSoup(html, 'html.parser')
    all=soup.find_all('tr',class_='odd')
    for i in all:
        t=i.find_all('td')
        ip=t[1].text+':'+t[2].text
        is_avail = checkip(targeturl,ip)
        if is_avail == True:
            proxies = {"http": "http://" + ip, "https": "https://" + ip}  # 代理ip
            # write(path=path,text=str(proxies))
            write(path=path, text=ip)
            # print(ip)


def get_proxies(target_url, ip_list):
    # log = Logger('spider.log', level='debug')
    "从ip代理池里筛选一个可用的代理ip"
    if len(ip_list) ==0:
        if excute_main(ipool_path):
            ip_list = get_ip_pool(ip_list)
            # get_proxies(target_url, ip_list)
    ip = random.choice(ip_list)
    #取出之后从代理池中直接remove掉
    # ip_list.remove(ip)
    if checkip(target_url, ip, 3):
        proxies = {"http": "http://" + ip, "https": "https://" + ip}  # 代理ip
        return proxies
    else:
        # log.logger.debug("移除此代理ip" + ip + "，换新代理，连接池剩余代理数量为" + str(len(ip_list)))
        log.logger.debug("换新代理，连接池剩余代理数量为" + str(len(ip_list)))
        if len(ip_list) > 0:
            ip_list.remove(ip)
            get_proxies(target_url, ip_list)
        else:
            log.logger.warning("代理池所有ip都不可用，正在更新代理池")
            if excute_main(ipool_path):
                ip_list = get_ip_pool(ip_list)
                get_proxies(target_url, ip_list)


def get_ip_pool(list):
    "获取ip代理池"
    ipool_path = os.path.dirname(os.path.dirname(__file__)) + '/docs/ip.txt'  # 存放爬取ip的文档path
    list.clear()
    f = open(ipool_path, "r")
    for line in f.readlines():
        if len(line.strip()) != 0:
            list.append(line)
    f.close()
    # if len(list) ==0:
    #     myname = socket.getfqdn(socket.gethostname())
    #     myaddr = socket.gethostbyname(myname)
    #     list.append(myaddr+":80")
    return list
#-----------------------------------------------------多线程抓取ip入口---------------------------------------------------
def getip(targeturl,path):
     truncatefile(path) # 爬取前清空文档
     start = datetime.datetime.now() # 开始时间
     threads=[]
     for type in range(4):   # 四种类型ip,每种类型取前三页,共12条线程
         for pagenum in range(3):
             t=threading.Thread(target=findip,args=(type+1,pagenum+1,targeturl,path))
             threads.append(t)
     log.logger.info('开始更新代理池')
     for s in threads: # 开启多线程爬取
         s.start()
     for e in threads: # 等待所有线程结束
         e.join()
     log.logger.info('更新完成')
     end = datetime.datetime.now() # 结束时间
     diff = gettimediff(start, end)  # 计算耗时
     ips = read(path)  # 读取爬到的ip数量
     log.logger.info('一共更新代理: %s 个,共耗时: %s \n' % (len(ips), diff))
def excute_main(path):
    # path = 'ip.txt'  # 存放爬取ip的文档path
    targeturl = 'http://www.cnblogs.com/TurboWay/'  # 验证ip有效性的指定url
    getip(targeturl, path)
    return True
#-------------------------------------------------------启动-----------------------------------------------------------
# ipool_path = os.path.dirname(os.path.dirname(__file__)) + '/docs/ip.txt'  # 存放爬取ip的文档path
# excute_main(ipool_path)