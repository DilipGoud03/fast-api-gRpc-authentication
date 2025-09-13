from sql.crud import users as user_crud
from google.protobuf.json_format import MessageToDict
import proto.users.users_pb2
import proto.users.users_pb2_grpc
import grpc
import database
import jwt
from datetime import datetime, timedelta
from helper.interceptor import RequestHeaderValidatorInterceptor


class UserService(proto.users.users_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.__db = database.get_db()
        self.__interceptor_service = RequestHeaderValidatorInterceptor()

    def __db_close(self):
        try:
            self.__db.close()
        except Exception as e:
            raise RuntimeError(
                f"Failed to close database connection: {str(e)}")

    def LoginUser(self, request, context):
        try:
            email = request.email
            _password = request.password
            user = user_crud.get_user_by_email(self.__db, email)
            status = False
            token = None
            if user:
                if user_crud._check_password(_password, user.password):
                    token = jwt.encode(
                        {
                            "exp": datetime.utcnow() + timedelta(days=7),
                            "iat": datetime.utcnow(),
                            "email": user.email,
                            "id": user.id,
                        },
                        "HelloWorld",
                        algorithm="HS256",
                    )
                    status = True
            self.__db_close()
            return proto.users.users_pb2.LoginUserResponse(
                token=token,
                status=status,
            )
        except grpc.RpcError as e:
            self.__db_close()
            raise RuntimeError(str(e))

    def GetUser(self, request, context):
        try:
            user = user_crud.get_user_by_id(self.__db, request.id)
            if not user:
                raise FileNotFoundError(
                    f"User with id {request.id} not found")
            logged_in_user = self.__interceptor_service._get_logged_in_user()
            if logged_in_user and logged_in_user.id != user.id:
                raise FileNotFoundError("Access denied")

            user = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            }
            self.__db_close()
            return proto.users.users_pb2.GetUserResponse(
                user=user
            )
        except grpc.RpcError as e:
            self.__db_close()
            raise RuntimeError(str(e))

    def CreateUser(self, request, context):
        try:
            user = MessageToDict(
                request.user, preserving_proto_field_name=True)
            user_exist = user_crud.get_user_by_email(self.__db, user['email'])
            if user_exist:
                raise ModuleNotFoundError("Provided email already exist, please use diffrent email")
            user = user_crud.create_user(self.__db, user)
            self.__db_close()
            return proto.users.users_pb2.CreateUserResponse(
                message="User created successfully"
            )
        except grpc.RpcError as e:
            self.__db_close()
            raise RuntimeError(str(e))

    def UpdateUser(self, request, context):
        try:
            logged_in_user = self.__interceptor_service._get_logged_in_user()
            if request.id != logged_in_user.id:
                raise PermissionError("Access denied")

            user_data= MessageToDict(request.user, preserving_proto_field_name=True)
            print("user_data", user_data)
            user = user_crud.get_user_by_id(self.__db, request.id)
            if not user:
                raise ValueError("User Not Found for provided id.")
                
            updated_user = user_crud.update_user(self.__db, user, user_data)
            print(user.__dict__)
            self.__db_close()
            return proto.users.users_pb2.UpdateUserResponse(
                user={}
            )
        except Exception as e:
            self.__db_close()
            raise PermissionError(str(e))
