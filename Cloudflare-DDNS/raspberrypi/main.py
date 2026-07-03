from cloudflare import Cloudflare
import getIPv6
import config

ipv6 = getIPv6.get_first_global_ipv6()
print("IPv6:", ipv6)

client = Cloudflare(
    api_token = config.CLOUDFLARE_API_TOKEN,
)

record_response = client.dns.records.update(
    dns_record_id = config.DNS_RECORD_ID_APIC,
    zone_id = config.ZONE_ID,
    name = config.DOMAIN_APIC,
    type = "AAAA",
    ttl = 60,
    content = ipv6
)
print(record_response)

record_response = client.dns.records.update(
    dns_record_id = config.DNS_RECORD_ID_WWW,
    zone_id = config.ZONE_ID,
    name = config.DOMAIN_WWW,
    type = "AAAA",
    ttl = 60,
    content = ipv6
)
print(record_response)