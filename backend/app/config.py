from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "my_shop"

    APP_SECRET_KEY: str = "change-me"
    ADMIN_USERNAME: str = "admin"
    # 默认值为 admin123 的 bcrypt hash，生产环境请在 .env 中覆盖 ADMIN_PASSWORD_HASH
    ADMIN_PASSWORD_HASH: str = "$2b$12$Rz7xO0w7Q2PPK/kFvsDsT.BhYAIdKe5aVCTnco.r.DTM1f8QxErjy"

    UPLOAD_DIR: str = "./uploads"
    CORS_ORIGINS: str = "*"

    model_config = {"env_file": ".env"}

    @model_validator(mode="after")
    def check_secret_key(self) -> "Settings":
        if self.APP_SECRET_KEY == "change-me":
            raise ValueError("APP_SECRET_KEY 不能使用默认值，请在 .env 中设置强密钥")
        return self


settings = Settings()
