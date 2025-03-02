from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

load_dotenv()


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class SuperUser(BaseModel):
    name: str
    email: str
    password: str
    username: str


class AuthJWT(BaseModel):
    private_key_path: Path
    public_key_path: Path
    algorithm: str
    access_token_expires_in_minutes: int


class RuntimeSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    # set it up according to your cpu
    workers: int = 1


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    products: str = "/products"
    manufacturers: str = "/manufacturers"
    auth: str = "/auth"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
    )
    runtime: RuntimeSettings = RuntimeSettings()
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()
    PROJECT_NAME: str
    environment: Environment
    auth: AuthJWT
    superuser: SuperUser


settings = Settings()  # type: ignore
