"""Inbound email provider implementations."""

from abc import ABC, abstractmethod
import imaplib
from email import message_from_bytes
from email.message import Message

from .config import Settings
from .email_parser import parse_email
from .exceptions import ConfigurationError
from .models import EmailMessage


class EmailReader(ABC):
    @abstractmethod
    def fetch(self) -> list[EmailMessage]:
        """Fetch normalized email messages."""


class DemoEmailReader(EmailReader):
    def __init__(self, messages: list[EmailMessage]) -> None:
        self.messages = messages

    def fetch(self) -> list[EmailMessage]:
        return list(self.messages)


class ImapEmailReader(EmailReader):
    """Read messages from IMAP without deleting or mutating them."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def fetch(self) -> list[EmailMessage]:
        if not self.settings.imap_username or not self.settings.imap_password.get_secret_value():
            raise ConfigurationError("IMAP username and password are required")
        client: imaplib.IMAP4 = (imaplib.IMAP4_SSL(self.settings.imap_host, self.settings.imap_port)
                                 if self.settings.imap_use_ssl else imaplib.IMAP4(self.settings.imap_host, self.settings.imap_port))
        try:
            client.login(self.settings.imap_username, self.settings.imap_password.get_secret_value())
            client.select(self.settings.imap_folder, readonly=True)
            status, data = client.search(None, "ALL")
            if status != "OK":
                return []
            messages: list[EmailMessage] = []
            for number in data[0].split():
                status, fetched = client.fetch(number, "(RFC822)")
                if status == "OK" and fetched and isinstance(fetched[0], tuple):
                    raw: Message = message_from_bytes(fetched[0][1])
                    messages.append(parse_email(raw, message_id=number.decode()))
            return messages
        finally:
            try:
                client.logout()
            except imaplib.IMAP4.error:
                pass
