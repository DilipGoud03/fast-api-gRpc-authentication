import collections
import grpc
import helper.generic_client_interceptor
from helper.interceptor import RequestHeaderValidatorInterceptor


class _ClientCallDetails(
    collections.namedtuple(
        "_ClientCallDetails", ("method", "timeout", "metadata", "credentials")
    ),
    grpc.ClientCallDetails,
):
    pass


def header_adder_interceptor(header, value):
    def intercept_call(
        client_call_details,
        request_iterator,
        request_streaming,
        response_streaming,
    ):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(
            (
                header,
                value,
            )
        )
        header_validator = RequestHeaderValidatorInterceptor()
        get_token_value = header_validator._get_logged_in_token()
        if get_token_value:
            get_token_value_exp = get_token_value.split(" ")
            if len(get_token_value_exp):
                if get_token_value_exp[0] == "Bearer":
                    metadata.append(
                        (
                            "authorization",
                            get_token_value,
                        )
                    )
                if get_token_value_exp[0] == "Basic":
                    metadata.append(
                        (
                            "x-auth-token",
                            get_token_value,
                        )
                    )
        get_super_user_value = header_validator._super_user()
        if get_super_user_value:
            metadata.append(
                (
                    "_as",
                    get_super_user_value,
                )
            )
        client_call_details = _ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
        )
        return client_call_details, request_iterator, None

    return helper.generic_client_interceptor.create(intercept_call)
