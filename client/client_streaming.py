import asyncio
import logging

import grpc
import hellostreamingworld_pb2
import hellostreamingworld_pb2_grpc


# greeting async generator
async def greeting(queue):
    name = await queue.get()
    if name:
        yield hellostreamingworld_pb2.HelloRequest(name=name)
    else:
        # if None is in the queue, finish the generator
        return


async def send_message(queue, count=5, interval=1):
    # simulating send message event
    print("send_msg start")
    for i in range(count):
        msg = f"message {i}"
        print(f"put {msg}")
        queue.put_nowait(msg)
        await asyncio.sleep(interval)
    # at the end of the messaging, send None to the queue
    await queue.put(None)

async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = hellostreamingworld_pb2_grpc.MultiGreeterStub(channel)

        queue = asyncio.Queue()
        task = asyncio.create_task(send_message(queue, count=30, interval=3))
        print("start grpc bidirectional streaming")
        while True:
            async for response in stub.SayMultiHello(greeting(queue)):
                print("Greeter client received: " + response.message)
            if task.done():
                print("done")
                break

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
