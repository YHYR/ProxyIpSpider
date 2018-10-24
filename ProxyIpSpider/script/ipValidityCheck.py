# -*- coding: utf-8 -*-
"""
代理Ip有效性校验

相对于爬取, IP的有效性校验比比较耗时的;
又因为Scrapy本身不支持并发, 所以在爬取IP的同时校验有效性会导致最终效率过于低下

可通过后台单独运行此脚本, 并基于进程池来提升校验效率
此处默认的进程数为10;校验等待超时时长为10s;

@Author YH YR
@Time 2018/10/24 17:19
"""
import random
import time

import multiprocessing
import requests

from ProxyIpSpider.utils.mysqlUtil import MysqlUtil
from ProxyIpSpider.utils.user_agents import agents

mysql = MysqlUtil('localhost', 'root', 'root', 'cloud_music_db', 3306)


class IPValidityCheck:
    @staticmethod
    def run(processes_num=10):
        """
        轮询代理IP表, 通过线程池提升IP筛选效率
        在一轮筛选过后,暂停5分钟后继续筛选
        :param processes_num:
        :return:
        """
        query_sql = 'select id, proxy_ip from proxy_ip_info'
        while True:
            results = mysql.query(query_sql, num='all')
            if len(results) == 0:
                print('IP table is empty')
                return
            pool = multiprocessing.Pool(processes=processes_num)
            for i in results:
                auto_increase_id = i[0]
                ip = i[1]
                pool.apply_async(proxy_ip_check, args=(ip, auto_increase_id))
            pool.close()
            pool.join()
            print('Cycle check per minutes')
            time.sleep(60)


def proxy_ip_check(check_ip, auto_increase_id, check_timeout=10):
    """
    代理IP有效性检验
    判断依据: 访问带爬取的目标地址, 根据请求返回结果初步判断有效性
    :param check_ip: 待检查IP
    :param auto_increase_id: 该数据在MySQL中对应的自增长Id
    :param check_timeout: 请求超时时长; 如果在该时间内请求无响应, 则认为此Ip无效
    :return:
    """
    delete_sql = 'delete from proxy_ip_info where id = {0}'.format(auto_increase_id)
    url = 'http://music.163.com/api/artist/top?offset=0&limit=100&total=false'
    proxies = {'http': check_ip}
    agent = random.choice(agents)
    header = {'Referer': 'https://music.163.com/',
              'User-Agent': agent}
    try:
        proxy_response = requests.get(url, proxies=proxies, headers=header, timeout=check_timeout)
        if proxy_response.status_code == 200:
            print('Valid IP: {0}'.format(check_ip))
        else:
            print('Invalid IP: {0}'.format(check_ip))
            mysql.modify(delete_sql.format(auto_increase_id))
    except:
        print('Invalid IP: {0}'.format(check_ip))
        mysql.modify(delete_sql.format(auto_increase_id))


if __name__ == '__main__':
    action = IPValidityCheck()
    action.run()
