import re
import json

import asyncio
import aiohttp
import aiofiles


async def make_request(website):
    async with aiohttp.ClientSession() as session:
        async with session.get(website) as response:
            return await response.text()


async def extract_ip_adress_from_html(loop, html):
    http_proxy_ip = []

    ip = await loop.run_in_executor(
        None, re.findall, r"((?:\d{1,3}\.){3}\d{1,3})", str(html)
    )

    http_proxy_ip.append(ip)

    return http_proxy_ip


async def write_ip_in_file(ips):
    async with aiofiles.open("proxy-list.txt", mode="w+") as txt_file:
        [await txt_file.write("\n".join(ip)) for ip in ips]


async def fetch_ips_from_website(website):
    html = await make_request(website)
    ips = await extract_ip_adress_from_html(asyncio.get_event_loop(), html)

    await write_ip_in_file(ips)


async def main(websites):
    tasks = [
        asyncio.get_event_loop().create_task(fetch_ips_from_website(website)) for website in websites
    ]

    [await task for task in tasks]

with open("datas.json") as f:
    datas = json.loads(f.read())
    proxy_collection_websites = datas["websites"]
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main(proxy_collection_websites))
