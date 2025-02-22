from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  database_hostname : str
  database_name : str
  database_username : str
  database_password : str
  secret_key : str
  jwt_algorithm : str
  token_expire_minutes : int
  
  class Config:
    env_file=".env"


settings = Settings()