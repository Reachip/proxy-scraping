import re
import asyncio
import aiohttp
import aiofiles


async def extract_html_page(loop, proxy_collection_from_websites):
    http_proxy_web_content = []
    socks_proxy_web_content = []

    async with aiohttp.ClientSession() as session:
        async with session.get(proxy_collection_from_websites["http"]) as response:
            http_proxy_web_content.append(await response.text())

        async with session.get(proxy_collection_from_websites["socks"]) as response:
            socks_proxy_web_content.append(await response.text())


    return http_proxy_web_content, socks_proxy_web_content


async def extract_ip_adress_from_html(loop, proxy_collection_from_websites):
    http_proxy_ip = []
    socks_proxy_ip = []

    http_proxy_collection_websites, socks_proxy_collection_websites = await extract_html_page(
        loop, proxy_collection_from_websites
    )

    for html_page in http_proxy_collection_websites:
        ip = await loop.run_in_executor(
            None, re.findall, r"((?:\d{1,3}\.){3}\d{1,3})", str(html_page)
        )
        http_proxy_ip.append(ip)

    for html_page in socks_proxy_collection_websites:
        ip = await loop.run_in_executor(
            None, re.findall, r"((?:\d{1,3}\.){3}\d{1,3})", str(html_page)
        )
        socks_proxy_ip.append(ip)

    return http_proxy_ip, socks_proxy_ip


async def write_ip_in_file(loop, proxy_collection_from_websites):

    http_proxy_ip, socks_proxy_ip = await extract_ip_adress_from_html(loop, proxy_collection_from_websites)

    async with aiofiles.open("proxy-list.txt", mode="w+") as txt_file:
        await txt_file.write("========= http proxy ============ \n")
        await txt_file.write("\n".join(http_proxy_ip[0]))
        await txt_file.write("\n ========= sockets proxy ============ \n")
        await txt_file.write("\n".join(socks_proxy_ip[0]))


async def main(loop, proxy_collection_from_websites):
    await asyncio.wait([
        write_ip_in_file(loop, proxy_collection_from_websites)
    ])

proxy_collection_from_websites = {
    "http": "https://free-proxy-list.net/",
    "socks": "https://www.socks-proxy.net/",
}

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, proxy_collection_from_websites))
