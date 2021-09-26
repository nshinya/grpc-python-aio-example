import asyncio
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    async def SayHello(
            self, request: helloworld_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    async def SayHelloAgain(
            self, request: helloworld_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message='Hello, %s again!' % request.name)

async def serve() -> None:
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())