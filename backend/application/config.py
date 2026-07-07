

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "trekking-management-secret-key"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery Configuration (NEW STYLE)
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"

    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]

    timezone = "Asia/Kolkata"
    enable_utc = True


    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = "harishcha456@gmail.com"
    MAIL_PASSWORD = "hgig tjis aplw ppcm"

    MAIL_DEFAULT_SENDER = "your_email@gmail.com"