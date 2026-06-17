import json
import logging
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def call_llm(system_prompt: str, user_prompt: str) -> dict:
    """Call Groq API and return the parsed JSON response dict."""
    client = AsyncGroq(api_key=settings.groq_api_key)

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=settings.llm_temperature,
        max_tokens=1024,
    )

    content = response.choices[0].message.content
    logger.debug(f"LLM raw response ({len(content)} chars): {content[:200]}...")
    return json.loads(content)
