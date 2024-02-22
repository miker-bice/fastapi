from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from . import schemas

SECRET_KEY = "733ed070966a3807a72ae7e0a1d48e2737baaafac37de6b632e3521d52702679"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30


oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp': expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return encoded_jwt

# decode the JWT
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenDataSchema(id=user_id)
    except JWTError:
        raise credentials_exception
    
    return token_data

# get the user for a protected endpoint
def get_current_user(token: str = Depends(oauth_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    return token_data
    