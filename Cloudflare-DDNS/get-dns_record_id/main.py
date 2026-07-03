from cloudflare import Cloudflare
import config

client = Cloudflare(
    api_token = config.CLOUDFLARE_API_TOKEN
)

records = client.dns.records.list(
    zone_id = config.ZONE_ID,
    name = config.DOMAIN,
    type = "AAAA",
)

for record in records:
    print("name:", record.name)
    print("type:", record.type)
    print("content:", record.content)
    print("id:", record.id)
    print()