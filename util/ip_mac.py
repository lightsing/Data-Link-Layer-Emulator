from socket import inet_aton, inet_ntoa


def ip2mac(ip) -> (str, bytes):
    if isinstance(ip, str):
        ip_bytes = inet_aton(ip)
    elif isinstance(ip, bytes):
        ip_bytes = ip
    else:
        raise TypeError('IP should be string or bytes')
    mac_bytes = b'\xff\xff' + ip_bytes
    mac_string = mac_bytes.hex().upper()
    mac_string = ':'.join((mac_string[i:i + 2] for i in range(0, len(mac_string), 2)))
    return mac_string, mac_bytes


def mac2ip(mac) -> str:
    if isinstance(mac, str):
        ip_bytes = bytes.fromhex(''.join(mac.split(':')[2:]))
    elif isinstance(mac, bytes):
        ip_bytes = mac[2:]
    else:
        raise TypeError('MAC should be string or bytes')
    return inet_ntoa(ip_bytes)
