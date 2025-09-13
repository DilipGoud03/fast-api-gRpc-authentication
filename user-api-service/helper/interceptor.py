import time
import grpc
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization as crypto_serialization
from decouple import config
import jwt
from helper.firewall import Firewall
from sql.models import users
from sql.schemas.logged_user import UserModel
# from sql.schemas.user.user_active import UserActiveSchema
import database
# from services.utility_service import UtilityService
import logging
# utility_service = UtilityService()


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class RequestHeaderValidatorInterceptor(grpc.ServerInterceptor):
    def __init__(
        self,
        code=grpc.StatusCode.UNAUTHENTICATED,
        details="Access denied!!",
    ):
        self._terminator = _unary_unary_rpc_terminator(code, details)
        self.__db = database.get_db()

    def intercept_service(self, continuation, handler_call_details):
        global token_global_variable
        token_global_variable = None
        global super_user
        super_user = None
        firewall = Firewall()
        if handler_call_details.method in firewall._ignore_security():
            return continuation(handler_call_details)
        for header, value in handler_call_details.invocation_metadata:
            if header == "_as":
                super_user = value
        for header, value in handler_call_details.invocation_metadata:
            if header == "authorization":
                if not self._decode_JWT(value):
                    return self._terminator
                return continuation(handler_call_details)
            if header == "x-auth-token":
                if not self._get_user_by_key(value):
                    return self._terminator
                return continuation(handler_call_details)
        return self._terminator

    def _decode_JWT(self, token: str) -> dict:
        global token_global_variable
        try:
            token_global_variable = token
            self.__db = database.get_db()
            token = token.split(" ")
            token = token[1]
            # public_key_pem = config("JWT_PUBLIC_KEY")
            # with open(public_key_pem, "rb") as key_file:
            #     public_key = key_file.read()
            try:
                decoded_token = jwt.decode(
                    token, "HelloWorld", algorithms=["HS256"])
            except Exception:
                raise print("Invalid token or expired token.")
            if decoded_token["exp"] >= time.time():
                user = self._current_user(decoded_token=decoded_token)
                user_dict = user.__dict__.copy()
                # remove SQLAlchemy internal key
                user_dict.pop('_sa_instance_state', None)
                try:
                    current_user = UserModel(**user_dict)
                except Exception as e:
                    print("Exception" + str(e))
                global user_global_variable
                user_global_variable = current_user
                # if super_user:
                #     if user_global_variable.roles:
                #         if (
                #             "ROLE_ADMIN" in user_global_variable.roles
                #             or "ROLE_COMPANY_ADMIN" in user_global_variable.roles
                #             or "ROLE_SUPER_ADMIN" in user_global_variable.roles
                #             or "ROLE_BRANCH_ADMIN" in user_global_variable.roles
                #         ):
                #             current_user = UserModel.model_validate(user)
                #             data = UserActiveSchema().dump(current_user)
                #             current_user = UserModel(**data)
                #             user_global_variable = current_user
                self.__db.close()
                return decoded_token
            else:
                return None
        except Exception:
            return None

    def _get_user_by_key(self, key):
        global token_global_variable
        token_global_variable = key
        self.__db = database.get_db()
        key = key.split(" ")
        key = key[1]
        key = utility_service._base64_decode(key)
        user = self.__db.query(users.User).filter(
            users.User.api_key == key).first()
        if user:
            current_user = UserModel.model_validate(user)
            global user_global_variable
            user_global_variable = current_user
            self.__db.close()
            return key
        else:
            self.__db.close()
            return None

    def _get_logged_in_user(self):
        return user_global_variable

    def _get_logged_in_token(self):
        return token_global_variable

    def _super_user(self):
        return super_user

    def _authenticate_role(self, permission, roles=None):
        rules = permission.split(",")
        if roles is None:
            roles = user_global_variable.roles
        else:
            roles = roles.split(",")

        for i in rules:
            if i in roles:
                return True
        return False

    def _current_user(self, decoded_token=None, key=None, s_user=None) -> UserModel:
        query = self.__db.query(users.User)
        user = None
        if decoded_token is not None:
            user = query.filter(users.User.id == decoded_token["id"])

        if key is not None:
            user = query.filter(users.User.api_key == key)

        if s_user is not None:
            user = query.filter(users.User.email == s_user)

        if user is not None:
            return user.first()
        return None
