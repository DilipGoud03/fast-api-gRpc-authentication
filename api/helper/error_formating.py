import grpc

class ErrorFormating():
    def _remove_data(message):
        message = message.replace(
            "grpc message Exception calling application:", "")
        message = message.replace("Exception calling application: ", "")
        return message

    def status_code(code):
        if code == grpc.StatusCode.NOT_FOUND:
            return 404
        elif code == grpc.StatusCode.ALREADY_EXISTS:
            return 409
        elif code == grpc.StatusCode.PERMISSION_DENIED:
            return 403
        elif code == grpc.StatusCode.UNAUTHENTICATED:
            return 401
        elif code == grpc.StatusCode.INVALID_ARGUMENT:
            return 422
        elif code == grpc.StatusCode.INTERNAL:
            return 500
        elif code == grpc.StatusCode.OK:
            return 200
        elif code == grpc.StatusCode.CANCELLED:
            return 499
        elif code == grpc.StatusCode.UNKNOWN:
            return 520
        elif code == grpc.StatusCode.DEADLINE_EXCEEDED:
            return 504
        elif code == grpc.StatusCode.RESOURCE_EXHAUSTED:
            return 429
        elif code == grpc.StatusCode.FAILED_PRECONDITION:
            return 400
        elif code == grpc.StatusCode.ABORTED:
            return 409
        elif code == grpc.StatusCode.OUT_OF_RANGE:
            return 400
        elif code == grpc.StatusCode.UNIMPLEMENTED:
            return 501
        elif code == grpc.StatusCode.INTERNAL:
            return 500
        elif code == grpc.StatusCode.UNAVAILABLE:
            return 503
        elif code == grpc.StatusCode.DATA_LOSS:
            return 500
        else:
            return 400