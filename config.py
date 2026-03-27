"""K-Mirror configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""  # Optional, can be set via .env
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_persist_dir: str = "./data/chroma_db"
    sqlite_db_path: str = "./data/unlearn.db"
    log_level: str = "INFO"

    # Scraping
    scrape_delay_seconds: float = 2.0
    jk_base_url: str = "https://jkrishnamurti.org"

    # Unlearning engine defaults
    default_question_ttl_days: int = 14
    deflected_question_ttl_days: int = 30
    explored_question_ttl_days: int = 7
    insight_decay_rate_per_month: float = 0.05
    insight_resurface_confidence_halving: float = 0.5
    insight_removal_threshold: float = 0.1

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
