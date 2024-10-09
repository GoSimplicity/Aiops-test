from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Ollama API 配置
    ollama_api_url: str = Field(default="http://localhost:11434", env="OLLAMA_API_URL")
    ollama_model_name: str = Field(default="llama3.2:3b", env="OLLAMA_MODEL_NAME")

    # 日志配置
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Kubernetes 配置
    kube_config_path: str = Field(default="./config.yaml", env="KUBE_CONFIG_PATH")

    class Config:
        env_file = ".env"
        extra = "forbid"  # 保持默认，禁止额外字段


settings = Settings()
