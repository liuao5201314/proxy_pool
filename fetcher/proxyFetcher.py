# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :   这是一个用于获取免费代理的工具类
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 初始版本
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
import execjs
from time import sleep


from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    获取免费代理的类
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        获取站大爷网站上的代理
        """

        target_url = "https://www.zdaye.com/free/1/"
        while target_url:
            _tree = WebRequest().get(target_url, verify=False).tree
            for tr in _tree.xpath("//table//tr"):
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)
            next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
            target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
            sleep(5)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        获取代理66网站上的代理
        """
        url = "http://www.66ip.cn/"
        resp = WebRequest().get(url, timeout=10).tree
        for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
            if i > 0:
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03():
        """ 开心代理
        获取开心代理网站上的代理
        """
        target_urls = ["http://www.kxdaili.com/dailiip/1/{}.html", "http://www.kxdaili.com/dailiip/2/{}.html"]
        for page_index in range(1, 5):
            for url in target_urls:
                tree = WebRequest().get(url.format(page_index), verify=False).tree
                for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                    ip = "".join(tr.xpath('./td[1]/text()')).strip()
                    port = "".join(tr.xpath('./td[2]/text()')).strip()
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy04():
        """ FreeProxyList https://www.freeproxylists.net/zh/
        获取FreeProxyList网站上的代理
        """
        url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
        tree = WebRequest().get(url, verify=False).tree
        from urllib import parse

        def parse_ip(input_str):
            html_str = parse.unquote(input_str)
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', html_str)
            return ips[0] if ips else None

        for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
            ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            if ip:
                yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=5):
        """ 快代理 https://www.kuaidaili.com
        获取快代理网站上的代理
        """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        # q:下面这一行是什么意思
        # a
        for page_index in range(1, 5):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            html = WebRequest().get(url)
            # 要停2秒,否则会被封
            sleep(2)
            #要从网页中js代码中提取ip和端口,找fpsList变量
            fps_list = re.findall(r'fpsList\s*=\s*(.*?);', html.text)
            #转为json格式
            if fps_list:
                proxy_list = json.loads(fps_list[0])
                for proxy in proxy_list:
                    yield "%s:%s" % (proxy['ip'], proxy['port'])

    @staticmethod
    def freeProxy06():
        """ 冰凌代理 https://www.binglx.cn
        获取冰凌代理网站上的代理
        """
        url = "http://www.binglx.cn/?page={}"
        # 从第一页开始获取,共获取5页
        for i in range(1, 5):
            try:
                tree = WebRequest().get(url.format(i)).tree
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])
            except Exception as e:
                print(e)


    @staticmethod
    def freeProxy07():
        """ 云代理
        获取云代理网站上的代理
        """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """ 小幻代理
        获取小幻代理网站上的代理
        """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """ 免费代理库
        获取免费代理库网站上的代理
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url, verify=False).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10():
        """ 89免费代理
        获取89免费代理网站上的代理
        """

        r = WebRequest().get("https://www.89ip.cn/index_1.html",timeout=10)
        response = r.response.text
        #如果第一次请求失败,说明第一次没有cookie,第二次请求带上cookie
        if r.response.status_code == 521:
            # 取出js方法
            # 取出js方法
            js_hanShu = re.findall('(function .*?)</script>', response)[0]
            print(js_hanShu)

            js_hanShu = str(js_hanShu).replace('eval("qo=eval;qo(po);")', 'return po')
            js_run = execjs.compile(js_hanShu)

            js_name = re.findall('setTimeout\("(.*?)\(', response)[0]
            # print('js_name:', js_name)
            js_arg = re.findall('setTimeout\("\D+\((\d+)\)",', response)[0]
            # print('js_arg:', js_arg)

            dCookie = js_run.call(js_name, js_arg)
            print(dCookie)

            ydclearance = re.findall('https_ydclearance=(.*?);', dCookie)[0]

            cookies = {
                'https_ydclearance': ydclearance,
            }
            r = WebRequest().get("https://www.89ip.cn/index_1.html", cookies=cookies, timeout=10)

        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

    @staticmethod
    def freeProxy11():
        """ 稻壳代理 https://www.docip.net/
        获取稻壳代理网站上的代理
        """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json['data']:
                yield each['ip']
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy12():
        """ pearApi https://api.pearktrue.cn/api/proxy/?type=getall/
        获取pearApi上的代理
        """
        r = WebRequest().get("https://api.pearktrue.cn/api/proxy/?type=getall", timeout=10)
        try:
            for each in r.json['data']:
                yield each['proxy']
        except Exception as e:
            print(e)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy03():
        print(_)

# http://nntime.com/proxy-list-01.htm
