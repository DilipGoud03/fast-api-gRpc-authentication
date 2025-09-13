class Firewall:
    def _ignore_security(self):
        return [
            "/",
            "/users.UserService/CreateUser",
            "/users.UserService/LoginUser"
        ]
