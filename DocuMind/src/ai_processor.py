"""Isolated OpenAI integration for document analysis."""

import os
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI

from .models import DocumentAnalysis
from .result_validator import ResultValidationError, validate_analysis


class AIProcessorError(Exception):
    """Raised for safe, user-facing AI processing failures."""


class MissingAPIKeyError(AIProcessorError):
    """Raised when OPENAI_API_KEY is unavailable."""


class AIProcessor:
    """Request and validate a concise structured document analysis."""

    def __init__(self, client: Any | None = None, model: str = "gpt-4o-mini") -> None:
        self.model = model
        if client is not None:
            self.client = client
            return
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise MissingAPIKeyError("OPENAI_API_KEY is not configured. Add it to your .env file.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AIProcessorError("OpenAI SDK is unavailable. Install dependencies with pip install -r requirements.txt.") from exc
        self.client = OpenAI(api_key=api_key)

    def analyze(self, document_text: str) -> DocumentAnalysis:
        if not document_text or not document_text.strip():
            raise AIProcessorError("Cannot analyze empty document text.")
        prompt = (
            "Analyze the following document. Return only a JSON object with exactly these "
            "fields: summary (string), key_points (non-empty array of strings), "
            "action_items (array of strings), document_category (string).\n\n"
            f"DOCUMENT:\n{document_text}"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You produce accurate JSON and no markdown."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            content = response.choices[0].message.content
            if not content:
                raise AIProcessorError("AI provider returned an empty response.")
            return validate_analysis(content)
        except (AIProcessorError, ResultValidationError) as exc:
            raise AIProcessorError(str(exc)) from exc
        except Exception as exc:
            raise AIProcessorError("AI processing failed. Please try again later.") from exc
