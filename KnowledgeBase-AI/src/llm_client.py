"""Language-model adapters used to generate grounded answers."""

from __future__ import annotations

import re
from typing import Protocol, Sequence

from .exceptions import LLMError
from .logger import get_logger
from .models import ConversationMessage, RetrievedChunk

GROUNDING_INSTRUCTIONS = (
    "You are a knowledge-base assistant. Answer using only the retrieved document context. "
    "If the context does not contain the answer, say that the indexed documents do not contain "
    "enough information. Do not invent facts, names, numbers, or sources."
)

INSUFFICIENT_ANSWER = (
    "The indexed documents do not contain enough information to answer this question."
)


class LLMClient(Protocol):
    def generate(
        self,
        question: str,
        chunks: Sequence[RetrievedChunk],
        history: Sequence[ConversationMessage],
    ) -> tuple[str, bool]: ...


class DemoLLMClient:
    """Extractive, offline answerer used for demos and tests."""

    def generate(
        self,
        question: str,
        chunks: Sequence[RetrievedChunk],
        history: Sequence[ConversationMessage],
    ) -> tuple[str, bool]:
        if not chunks:
            return INSUFFICIENT_ANSWER, False
        _ = history
        query_tokens = _tokens(question)
        if not query_tokens:
            return INSUFFICIENT_ANSWER, False
        scored_sentences: list[tuple[int, str]] = []
        for retrieved in chunks:
            for sentence in _sentences(retrieved.chunk.text):
                overlap = len(query_tokens.intersection(_tokens(sentence)))
                if overlap:
                    scored_sentences.append((overlap, sentence))
        scored_sentences.sort(key=lambda item: item[0], reverse=True)
        unique: list[str] = []
        seen: set[str] = set()
        for overlap, sentence in scored_sentences:
            if overlap < 2:
                continue
            key = sentence.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(sentence)
            if len(unique) == 1:
                break
        if not unique:
            return INSUFFICIENT_ANSWER, False
        names = ", ".join(dict.fromkeys(item.chunk.document_name for item in chunks))
        return f"{' '.join(unique)} (Sources: {names})", True


class OpenAILLMClient:
    """Chat Completions adapter. The SDK is imported only when this client is used."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        if not api_key:
            raise LLMError("OPENAI_API_KEY is required for OpenAI generation.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMError(
                "OpenAI SDK is unavailable. Install dependencies with pip install -r requirements.txt."
            ) from exc
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.logger = get_logger()

    def generate(
        self,
        question: str,
        chunks: Sequence[RetrievedChunk],
        history: Sequence[ConversationMessage],
    ) -> tuple[str, bool]:
        context = build_context(chunks)
        messages = [{"role": "system", "content": GROUNDING_INSTRUCTIONS}]
        for item in history[-8:]:
            messages.append({"role": item.role, "content": item.content})
        messages.append(
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\nRetrieved context:\n{context}\n\n"
                    "Answer the question using only the retrieved context."
                ),
            }
        )
        self.logger.info("Requesting a grounded answer from the AI provider")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
            )
            content = (response.choices[0].message.content or "").strip()
            if not content:
                raise LLMError("AI provider returned an empty response.")
            grounded = INSUFFICIENT_ANSWER.lower() not in content.lower()
            if not chunks:
                grounded = False
            return content, grounded
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError("AI provider failed. Please try again later.") from exc


def build_context(chunks: Sequence[RetrievedChunk]) -> str:
    if not chunks:
        return "(no retrieved context)"
    parts: list[str] = []
    for index, retrieved in enumerate(chunks, start=1):
        chunk = retrieved.chunk
        page = f", page {chunk.page_number}" if chunk.page_number else ""
        header = f"[{index}] {chunk.document_name} ({chunk.chunk_id}{page})"
        parts.append(f"{header}\n{chunk.text}")
    return "\n\n".join(parts)


_STOPWORDS = {
    "the",
    "and",
    "for",
    "are",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "that",
    "this",
    "with",
    "from",
    "each",
    "how",
    "many",
    "does",
    "did",
    "can",
    "about",
    "into",
    "your",
    "our",
    "their",
    "current",
    "company",
    "companies",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in _STOPWORDS
    }


def _sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [piece.strip() for piece in pieces if piece.strip()]
