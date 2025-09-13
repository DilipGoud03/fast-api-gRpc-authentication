import time
from decouple import config
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


def decodeJWT(token: str) -> dict:
    try:
        try:
            decoded_token = jwt.decode(token, "HelloWorld", algorithms=["HS256"])
        except Exception:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        return decoded_token is not None if decoded_token["exp"] >= time.time() else None
    except Exception:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        global auth_type
        auth_type = "Bearer"
        global jwt_token
        jwt_token = None
        global super_user
        super_user = None
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request): # type: ignore
        try:
            global auth_type
            auth_type = "Bearer"
            credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self
            ).__call__(request) # type: ignore
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=403, detail="Invalid authentication scheme."
                    )
                if credentials.scheme == "Bearer":
                    if not self.verify_jwt(credentials.credentials, request):
                        raise HTTPException(
                            status_code=403, detail="Invalid token or expired token."
                        )
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid authorization code."
                )
        except Exception as e:
            print(e)
        credentials = request.headers.get("x-auth-token")
        global jwt_token
        
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        auth_type = "Basic"
        jwt_token = credentials
        request_args = dict(request.query_params)
        global super_user
        super_user = None
        if "_as" in request_args:
            super_user = request_args["_as"]
        return jwt_token

    def verify_jwt(self, jwtToken: str, request: Request) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtToken)
            global jwt_token
            jwt_token = jwtToken
            request_args = dict(request.query_params)
            global super_user
            super_user = None
            if "_as" in request_args:
                super_user = request_args["_as"]
        except Exception:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    def _get_token():
        print("Herer")
        if auth_type and jwt_token:
            return auth_type + " " + jwt_token

    def _super_user():
        return super_user
