import grpc
from helper import header_manipulator_client_interceptor


class ConnectionChannel():

    async def user_channel(self):
        header_adder_interceptor = (
            header_manipulator_client_interceptor.header_adder_interceptor()
        )
        channel = grpc.insecure_channel("localhost:50061")
        """Create a gRPC channel for user service."""
        return grpc.intercept_channel(channel, header_adder_interceptor)

    async def contact_channel(self):
        header_adder_interceptor = (
            header_manipulator_client_interceptor.header_adder_interceptor
        )
        channel = grpc.insecure_channel("localhost:50062")
        """Create a gRPC channel for contact service."""
        return grpc.intercept_channel(channel, header_adder_interceptor)
