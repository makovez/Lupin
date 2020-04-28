from threading import Lock

class ProxyAPI:
    pass

class Proxy:
    def __init__(self):
        self.host = ""
        self.busy = False
        self.failures=0


class Proxies(ProxyAPI):
    lock = Lock()
    
    def __init__(self,maxfails=3):
        self.proxies = []
        self.maxfailures=maxfails
    
    def add_proxy(self, proxy: Proxy):
        self.proxies.append(proxy)

    def add_proxy(self,pl):
        for p in pl:
            if p.isinstance(Proxy):
                self.proxies.append(p)

    def clear_all(self):
        lock.acquire()
        Proxies.free()
        lock.release()

    def remove_fail_proxies(self):
        lock.acquire()
        for p in self.proxies: 
            if not p.busy and p.failures > self.maxfailures:
                self.proxies.remove(p)
        lock.release()

    def get_proxy(self):
        lock.acquire()
        proxy = next((proxy for proxy in self.proxies if not proxy.busy and proxy.failures<3), None)
        if proxy:
            proxy.busy = True
        lock.release()
        return proxy

def run():
    pass