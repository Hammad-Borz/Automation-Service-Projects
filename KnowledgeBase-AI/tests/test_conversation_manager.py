from src.conversation_manager import ConversationManager
from src.models import SourceCitation


def test_records_turns_and_expands_short_follow_ups() -> None:
    manager = ConversationManager(max_messages=6)
    manager.add_user("How many PTO days do employees receive?")
    manager.add_assistant(
        "Employees receive 20 days.",
        [SourceCitation(document_id="doc_1", document_name="handbook.pdf", chunk_id="chunk_1", score=0.8)],
    )
    expanded = manager.expand_query("What about remote work?")
    assert "PTO days" in expanded
    assert "remote work" in expanded
    assert manager.last_user_message() == "How many PTO days do employees receive?"
    assert manager.history()[1].sources[0].document_name == "handbook.pdf"


def test_trims_history_and_clears() -> None:
    manager = ConversationManager(max_messages=4)
    for index in range(6):
        manager.add_user(f"question {index}")
        manager.add_assistant(f"answer {index}")
    assert len(manager.history()) == 4
    manager.clear()
    assert manager.history() == []
    assert manager.last_user_message() is None
