from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    '''
    returns a str(hashed password)
    password:str - password to be hashed
    '''
    hashed_password = pwd_context.hash(password)

    return hashed_password

def verify(raw_password, hashed_password) -> bool:
    '''
    returns a boolean
    raw_password:str - raw input password by the user
    hashed_password:str - hashed password
    '''
    return pwd_context.verify(raw_password, hashed_password)