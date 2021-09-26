import asyncio
from asyncio.queues import QueueEmpty

async def generator(queue):
    try:
        yield queue.get_nowait()
    except QueueEmpty:
        await asyncio.sleep(0)

async def put_items(queue, count=5, interval=1):
    print("start put items")
    for i in range(count):
        queue.put_nowait(i)
        await asyncio.sleep(interval)

async def main():
    queue = asyncio.Queue()
    task = asyncio.create_task(put_items(queue))
    while True:
        async for msg in generator(queue):
            print(msg)
        if task.done():
            break

asyncio.run(main())
