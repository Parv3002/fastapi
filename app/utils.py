from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password:str):
    return pwd_context.hash(password)

def validate(user_input_password,original_password):
    return pwd_context.verify(user_input_password,original_password)