"""
Example usage of aiohttp client session and how it works
"""

import time

import asyncio
import aiohttp


def get_time_ms():
    """Return the current time in ms"""
    return int(round(time.time() * 1000))


async def fetch(session, url):
    """Fetch the given url with the client session"""
    async with session.get(url) as response:
        return await response.text()


async def save_website(session, url, name):
    """Save the website response to a file"""

    local_start_time = get_time_ms()

    html = await fetch(session, url)
    with open(name, "w") as f:
        f.write(str(html))

    print(f"Time to get {name} was {get_time_ms() - local_start_time}")


async def main():
    """
    Asynchronously get 4 webpages and time how long it took for
    each one individually and for all of them together
    """
    # Initialize the client session
    client_session = aiohttp.ClientSession()

    start_time = get_time_ms()

    coros = [
        save_website(client_session, "https://www.python.org", "python-org.html"),
        save_website(client_session, "https://www.chipy.org/", "chipy.html"),
        save_website(client_session, "https://us.pycon.org/2020/", "pycon-2020.html"),
        save_website(
            client_session, "https://python.ie/pycon-2019/", "pyconie-2019.html"
        ),
    ]

    await asyncio.gather(*coros)

    print(f"The total time to get all webpages was {get_time_ms() - start_time}")
    await client_session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
