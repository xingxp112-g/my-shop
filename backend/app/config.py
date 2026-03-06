from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "my_shop"

    APP_SECRET_KEY: str = "change-me"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    UPLOAD_DIR: str = "./uploads"

    model_config = {"env_file": ".env"}


settings = Settings()
