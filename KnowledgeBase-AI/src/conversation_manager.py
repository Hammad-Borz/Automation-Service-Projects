"""Session-scoped conversation history for follow-up questions."""

from __future__ import annotations

from .models import ConversationMessage, SourceCitation


class ConversationManager:
    def __init__(self, max_messages: int = 20) -> None:
        if max_messages < 2:
            raise ValueError("max_messages must be at least 2")
        self.max_messages = max_messages
        self._messages: list[ConversationMessage] = []

    def add_user(self, content: str) -> ConversationMessage:
        message = ConversationMessage(role="user", content=content)
        self._append(message)
        return message

    def add_assistant(
        self, content: str, sources: list[SourceCitation] | None = None
    ) -> ConversationMessage:
        message = ConversationMessage(role="assistant", content=content, sources=sources or [])
        self._append(message)
        return message

    def history(self) -> list[ConversationMessage]:
        return list(self._messages)

    def last_user_message(self) -> str | None:
        for message in reversed(self._messages):
            if message.role == "user":
                return message.content
        return None

    def clear(self) -> None:
        self._messages.clear()

    def expand_query(self, question: str) -> str:
        """Combine a follow-up question with the previous user turn for retrieval."""
        previous = None
        for message in reversed(self._messages):
            if message.role == "user" and message.content != question:
                previous = message.content
                break
        if previous and len(question.split()) <= 8:
            return f"{previous} {question}"
        return question

    def _append(self, message: ConversationMessage) -> None:
        self._messages.append(message)
        overflow = len(self._messages) - self.max_messages
        if overflow > 0:
            self._messages = self._messages[overflow:]
