

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM ──────────────────────────────────────────
    llm_provider: str = Field(default="groq")
    llm_model: str = Field(default="llama-3.1-70b-versatile")
    llm_temperature: float = Field(default=0.3)

    groq_api_key: str = Field(default="")

    use_usda_fallback: bool = Field(default=True)

    # ── Database ─────────────────────────────────────
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/pal_ai.db"
    )

    @property
    def active_api_key(self) -> str:
        if self.llm_provider == "groq":
            return self.groq_api_key
        return self.openai_api_key


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
