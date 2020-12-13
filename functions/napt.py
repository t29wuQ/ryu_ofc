import random

class NAPT:
    ports = [] 
    origin_map = {}
    napt_map = {}

    def new_port(self, ip_src, port_src):
        if port_src in NAPT.napt_map:
            return NAPT.napt_map[port_src]
        start = 1024
        end = 49151
        port = random.randrange(start, end)
        while port in NAPT.ports:
            port = random.randrange(start, end)
        NAPT.ports.append(port)
        NAPT.origin_map[port] = [ip_src, port_src]
        NAPT.napt_map[port_src] = port
        return port

    def get_origin_ip(self, port):
        return NAPT.origin_map[port][0]
    
    def get_origin_port(self, port):
        return NAPT.origin_map[port][1]

def new_port(ip_src, port_src):
    return NAPT().new_port(ip_src, port_src)

def get_origin_ip(port_dst):
    return NAPT().get_origin_ip(port_dst)

def get_origin_port(port_dst):
    return NAPT().get_origin_port(port_dst)