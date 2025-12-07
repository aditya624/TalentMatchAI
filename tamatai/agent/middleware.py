import logging
from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain_core.language_models.chat_models import BaseChatModel

from tamatai.config import settings

logger = logging.getLogger(__name__)


class ModelRouterMiddleware(AgentMiddleware):
    """
    Middleware class to retry Groq then fall back to a provided OpenAI model instance.
    """

    def __init__(self, fallback_model: BaseChatModel):
        self.fallback_model = fallback_model

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        last_error: Exception | None = None
        retries = max(0, settings.groq.retry_count)

        for attempt in range(retries):
            try:
                return handler(request)
            except Exception as exc:
                last_error = exc
                logger.warning("Groq call failed (attempt %s/%s): %s", attempt + 1, retries, exc)

        if not settings.openai.api_key:
            raise RuntimeError(
                f"Groq failed after {retries} attempt(s) and no OPENAI_API_KEY is configured for fallback"
            ) from last_error

        try:
            return handler(request.override(model=self.fallback_model))
        except Exception as exc:
            raise RuntimeError(
                f"Groq failed after {retries} attempt(s) and fallback to OpenAI model '{self.fallback_model.model_name}' also failed"
            ) from (
                last_error or exc
            )
