import re
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


async def write_ip_in_file(loop, ips):
    async with aiofiles.open("proxy-list.txt", mode="w+") as txt_file:
        [await txt_file.write("\n".join(ip)) for ip in ips]


async def fetch_ips_from_website(loop, website):
    html = await make_request(website)
    ips = await extract_ip_adress_from_html(loop, html)
    await write_ip_in_file(loop, ips)


async def main(loop, websites):
    tasks = [
        loop.create_task(fetch_ips_from_website(loop, website)) for website in websites
    ]

    for task in tasks:
        await task


proxy_collection_websites = (
    "https://free-proxy-list.net/",
    "http://www.gatherproxy.com/",
    "https://proxyhttp.net/",
    "http://spys.one/en/",
    "http://proxy-list.org/french/index.php",
)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, proxy_collection_websites))
