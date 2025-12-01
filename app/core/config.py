from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    PROJECT_NAME: str = "API GammeConnect"
    DATABASE_URL: str = "postgresql://postgres:12345@localhost:5432/gameconnect"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    STEAM_API_KEY: str | None = None

    # SendGrid
    SENDGRID_API_KEY: str
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str | None = None
    FRONTEND_URL: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

<<<<<<< HEAD
settings = Settings()from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    PROJECT_NAME: str = "API GameConnect"

    # A Railway injeta o DATABASE_URL automaticamente
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    STEAM_API_KEY: str | None = None

    # SENDGRID
    SENDGRID_API_KEY: str
    MAIL_FROM: EmailStr
    MAIL_FROM_NAME: str | None = None
    FRONTEND_URL: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

=======
settings = Settings()
>>>>>>> e5b4ec757330ba6b79850b145dd2efb94bc877a9
