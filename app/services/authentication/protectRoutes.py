from fastapi import HTTPException,Depends
from services.authentication.auth_services import decode_access_token
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str=Depends(oauth2_scheme)):
    data = decode_access_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return data