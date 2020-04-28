import requests
from bs4 import BeautifulSoup

url = "https://www.firexproxy.com/"

class Proxy:
    def __init__(self, ip, port, protocol, ping):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.ping = ping

    

class ProxyAPI:

    def __init__(self):
        self.session = requests.Session()

    def get_page(self):
        page = self.session.get(url).text
        return page

    def get_info_proxy(self, elem):
        proxy_info = {
            '2': None,
            '3': None,
            '4': None,
            '5': None
        }
        for info in elem.findChildren():
            if not info.has_attr("aria-colindex"):
                continue

            if info["aria-colindex"] in proxy_info:
                proxy_info[info["aria-colindex"]] = info.text

        return proxy_info


    def build_proxy(self, data):
        proxy_info = self.get_info_proxy(data)
        ip = proxy_info['2']
        port = proxy_info['3']
        protocol = proxy_info['4']
        ping = proxy_info['5']

        proxy = {ip: Proxy(ip, port, protocol, ping)}

        return proxy

    def get_proxies(self):
        proxies = {}

        page = self.get_page()
        soup = BeautifulSoup(page, 'html.parser')
        for child in soup.tbody.findChildren():
            for elem in child.findChildren():
                if elem.has_attr("aria-colindex"):
                    proxy = self.build_proxy(child)
                    proxies.update(proxy)
                    
        return proxies



proxy = ProxyAPI()
print(proxy.get_proxies())
        