"""
Example usage of asyncio and how it works and is implemented
"""

import asyncio
import time


START = int(time.time())


def time_difference():
    """Return the different in time between now and the start time"""
    return int(time.time()) - START


async def heavy_task_1():
    """Heavy task that takes 7 seconds to complete"""

    print(f"heavy_task_1 starting at {time_difference()} seconds")
    await asyncio.sleep(7)
    print(f"heavy_task_1 finished after {time_difference()} seconds")


async def heavy_task_2():
    """Heavy task that takes 2 seconds to complete"""

    print(f"heavy_task_2 starting at {time_difference()} seconds")
    await asyncio.sleep(2)
    print(f"heavy_task_2 finished after {time_difference()} seconds")


async def heavy_task_3():
    """Heavy task that takes 3 seconds to complete"""

    print(f"heavy_task_3 starting at {time_difference()} seconds")
    await asyncio.sleep(3)
    print(f"heavy_task_3 finished after {time_difference()} seconds")


async def heavy_task_4():
    """Heavy task that takes 1 seconds to complete"""

    print(f"heavy_task_4 starting at {time_difference()} seconds")
    await asyncio.sleep(1)
    print(f"heavy_task_4 finished after {time_difference()} seconds")


async def coro_test():
    print("\nthis is a coroutine\n")


async def main():
    """The main function"""

    # Notice how this isn't printing the text from the coro_test
    # This is because we didn't await the coroutine. The coroutine
    # Wasn't run, it was kept as a coroutine for us to run later.
    coro = coro_test()
    print(coro)

    # This will actually run the function because it was awaited
    await coro

    # Notice how we're not awaiting any of the function calls here
    # That's because asyncio.gather takes in coroutines and runs them for us
    # It'll run take all the coroutines and run then until they all finish.
    # Only then will it proceed. The coroutines are run asynchronously here.
    await asyncio.gather(heavy_task_1(), heavy_task_2(), heavy_task_3(), heavy_task_4())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("\nFinished!")
