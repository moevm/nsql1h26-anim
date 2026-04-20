from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  app_host: str
  app_port: int
  
  app_react_host: str
  app_react_port: int

  jwt_secret: str
  jwt_algorithm: str
  access_token_expire_minutes: int
  refresh_token_expire_days: int
  
  neo4j_uri: str  
  neo4j_user: str
  neo4j_password: str

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()