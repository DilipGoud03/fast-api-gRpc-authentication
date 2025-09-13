import grpc
from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, Depends, HTTPException
import proto.users.users_pb2
import proto.users.users_pb2_grpc
from fastapi.responses import JSONResponse
import typing as t
from helper.connections import ConnectionChannel
from helper.error_formating import ErrorFormating
from helper.auth import JWTBearer
from models.users import User, UserLogin, UserUpdate


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
def create_user(
    user: User,
    channel: t.Any = Depends(ConnectionChannel().user_channel)
) -> JSONResponse:
    client = proto.users.users_pb2_grpc.UserServiceStub(channel)
    try:
        user = user.model_dump()
        response = client.CreateUser(
            proto.users.users_pb2.CreateUserRequest(user=user)
        )
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=400, detail=ErrorFormating._remove_data(e.details()))

    response = MessageToDict(response, preserving_proto_field_name=True)
    return response


@router.get("/{id}", status_code=200)
def get_user(
    id: int,
    d: t.Any = Depends(JWTBearer()),
    channel: t.Any = Depends(ConnectionChannel().user_channel)
) -> JSONResponse:
    client = proto.users.users_pb2_grpc.UserServiceStub(channel)
    try:

        response = client.GetUser(proto.users.users_pb2.GetUserRequest(id=id))
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=404, detail=ErrorFormating._remove_data(e.details()))

    response = MessageToDict(response, preserving_proto_field_name=True)
    return response['user']


@router.post("/login", status_code=200)
def login_user(
    credential: UserLogin,
    channel: t.Any = Depends(ConnectionChannel().user_channel)
) -> JSONResponse:
    client = proto.users.users_pb2_grpc.UserServiceStub(channel)
    try:
        response = client.LoginUser(
            proto.users.users_pb2.LoginUserRequest(
                email=credential.email,
                password=credential.password)
        )
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=400, detail=ErrorFormating._remove_data((e.details())))

    response = MessageToDict(
        response, preserving_proto_field_name=True, including_default_value_fields=True)
    if response["status"] == True:
        return response
    else:
        raise HTTPException(
            status_code=400, detail="Bad credentials")


@router.put("/{id}", status_code=200)
def update_user(
    id: int,
    user: UserUpdate,
    d: t.Any = Depends(JWTBearer()),
    channel: t.Any = Depends(ConnectionChannel().user_channel)
) -> JSONResponse:
    client = proto.users.users_pb2_grpc.UserServiceStub(channel)
    try:
        user = user.model_dump()
        grpc_r = proto.users.users_pb2.UpdateUserRequest(
            id=id,
            user=user
        )
        response = client.UpdateUser(grpc_r)

    except grpc.RpcError as e:
        raise HTTPException(
            status_code=400, detail=ErrorFormating._remove_data(e.details()))

    response = MessageToDict(response, preserving_proto_field_name=True)
    return response['user']
