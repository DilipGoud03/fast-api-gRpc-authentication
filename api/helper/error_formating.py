class ErrorFormating():
    def _remove_data(message):
        message = message.replace(
            "grpc message Exception calling application:", "")
        message = message.replace("Exception calling application: ", "")
        return message
