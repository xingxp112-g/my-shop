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

    model_config = {"env_file": ".env"}


settings = Settings()
