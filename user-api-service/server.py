from concurrent import futures
from helper.interceptor import RequestHeaderValidatorInterceptor
import logging

import grpc
import proto.users.users_pb2
import proto.users.users_pb2_grpc
import services.users
import asyncio


async def serve():
    header_validator = RequestHeaderValidatorInterceptor(
        grpc.StatusCode.UNAUTHENTICATED,
        "Access denied!!!",
    )
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(header_validator,),
    )
    port = "50061"
    proto.users.users_pb2_grpc.add_UserServiceServicer_to_server(
        services.users.UserService(), server
    )
    server.add_insecure_port("[::]:" + port)
    logging.info("Starting server on %s", "[::]:" + port)

    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    print("gRPC user server started")
    asyncio.run(serve())
