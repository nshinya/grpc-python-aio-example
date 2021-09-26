import asyncio
from asyncio.queues import QueueEmpty
import logging

import grpc
import hellostreamingworld_pb2
import hellostreamingworld_pb2_grpc

queue = asyncio.Queue()

async def send_message(queue, interval=10):
    # simulating send message event
    print("send_msg start")
    i = 0
    while True:
        msg = f"message {i} from server"
        print(f"put {msg}")
        queue.put_nowait(msg)
        i += 1
        await asyncio.sleep(interval)

class Greeter(hellostreamingworld_pb2_grpc.MultiGreeterServicer):
    async def SayHello(
            self, request: hellostreamingworld_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> hellostreamingworld_pb2.HelloReply:
        yield hellostreamingworld_pb2.HelloReply(message=f'Hello, {request.name}!')

    async def SayMultiHello(self, request_iterator, context):
        print("start SayMultiHello")
        # receive client stream data
        async for request in request_iterator:
            print("yield response")
            yield hellostreamingworld_pb2.HelloReply(message=f'Hello, {request.name}!')
        # send server stream data in the queue
        try:
            while True:
                msg = queue.get_nowait()
                yield hellostreamingworld_pb2.HelloReply(message=msg)
        except QueueEmpty:
            pass

async def serve() -> None:
    server = grpc.aio.server()
    hellostreamingworld_pb2_grpc.add_MultiGreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    task = asyncio.create_task(send_message(queue))
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
