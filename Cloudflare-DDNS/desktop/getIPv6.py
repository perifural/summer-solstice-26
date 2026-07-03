import psutil
import socket
import ipaddress


def get_global_ipv6_addresses():
    """
    Get all global IPv6 addresses from local network interfaces.
    Filters out link-local, loopback, private, multicast, and invalid IPv6 addresses.
    """
    ipv6_addresses = []

    for interface_name, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET6:
                raw_ip = addr.address

                # Windows may return IPv6 like: fe80::abcd%12
                # Remove the zone index after %
                ip = raw_ip.split("%")[0]

                try:
                    ip_obj = ipaddress.IPv6Address(ip)
                except ValueError:
                    continue

                if ip_obj.is_global:
                    ipv6_addresses.append({
                        "interface": interface_name,
                        "ipv6": ip,
                        "raw": raw_ip
                    })

    return ipv6_addresses


def get_first_global_ipv6():
    """
    Return the first global IPv6 address found.
    Useful for DDNS.
    """
    addresses = get_global_ipv6_addresses()

    if not addresses:
        return None

    return addresses[0]["ipv6"]


if __name__ == "__main__":
    ipv6_list = get_global_ipv6_addresses()

    if not ipv6_list:
        print("No global IPv6 address found.")
    else:
        print("Global IPv6 addresses found:")

        for item in ipv6_list:
            print(f"{item['interface']}: {item['ipv6']}")

        print()
        print(f"First usable IPv6 for DDNS: {get_first_global_ipv6()}")