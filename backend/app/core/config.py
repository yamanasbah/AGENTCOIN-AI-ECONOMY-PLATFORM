from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AgentCoin AI Economy"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"

    postgres_dsn: str = "postgresql+psycopg2://agentcoin:agentcoin@db:5432/agentcoin"
    redis_url: str = "redis://redis:6379/0"
    token_symbol: str = "AGC"
    token_min_stake: float = 50.0
    token_agent_creation_burn: float = 10.0

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
