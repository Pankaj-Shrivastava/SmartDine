import logging
from functools import lru_cache
from typing import Self
# pyrefly: ignore [missing-import]
from pydantic import Field, model_validator, ValidationError
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    groq_api_key: str = Field(..., description="Groq API key")
    llm_model: str = Field("llama-3.3-70b-versatile", description="LLM model override")
    llm_temperature: float = Field(0.3, ge=0.0, le=2.0, description="Temperature for generation")
    budget_low_max: int = Field(300, ge=0, description="Max budget for 'low'")
    budget_medium_max: int = Field(800, ge=0, description="Max budget for 'medium'")
    max_candidates: int = Field(20, ge=3, description="Max candidate rows passed to LLM")
    log_level: str = Field("INFO", description="Log level")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

    @model_validator(mode="after")
    def validate_budget_thresholds(self) -> Self:
        if self.budget_low_max >= self.budget_medium_max:
            raise ValueError(
                f"BUDGET_LOW_MAX ({self.budget_low_max}) must be strictly less than BUDGET_MEDIUM_MAX ({self.budget_medium_max})"
            )
        return self

@lru_cache()
def get_settings() -> Settings:
    """Load and validate system settings. Raises descriptive RuntimeError on failures."""
    try:
        return Settings()
    except ValidationError as e:
        errors = e.errors()
        missing_fields = [err["loc"][0] for err in errors if err["type"] == "missing"]
        
        if "groq_api_key" in missing_fields:
            raise RuntimeError(
                "\n========================================================================\n"
                "CONFIGURATION ERROR: 'GROQ_API_KEY' is missing.\n"
                "1. Sign up for a free key at: https://console.groq.com/\n"
                "2. Create a '.env' file in the root directory (copied from .env.example)\n"
                "3. Set GROQ_API_KEY=your_actual_api_key\n"
                "========================================================================"
            ) from e
            
        # Compile other validation errors
        error_details = []
        for err in errors:
            loc = " -> ".join(str(l) for l in err["loc"])
            msg = err["msg"]
            error_details.append(f"- {loc}: {msg}")
            
        raise RuntimeError(
            f"Configuration validation failed:\n" + "\n".join(error_details)
        ) from e
