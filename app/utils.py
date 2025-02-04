from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def password_hash(password : str):
  return pwd_context.hash(password)

def verify_password(registered_password : str,password : str):
  return pwd_context.verify(password,registered_password)