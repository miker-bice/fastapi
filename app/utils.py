from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    '''
    returns a str(hashed password)
    password:str - password to be hashed
    '''
    hashed_password = pwd_context.hash(password)

    return hashed_password