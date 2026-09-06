"""MailFlow command-line demonstration entry point."""

from .config import get_settings
from .demo_data import demo_emails
from .email_reader import DemoEmailReader
from .logger import configure_logging
from .response_generator import DemoResponseGenerator
from .workflow import EmailWorkflow


def main() -> None:
    settings = get_settings()
    logger = configure_logging(settings)
    reader = DemoEmailReader(demo_emails())
    workflow = EmailWorkflow(response_generator=DemoResponseGenerator(), logger=logger)
    emails = reader.fetch()
    results = workflow.process_many(emails)

    print("\nMailFlow - Intelligent Email Automation System")
    print("=" * 50)
    print(f"Demo mode: {settings.demo_mode} | Received: {len(emails)} emails\n")
    for email, result in zip(emails, results):
        action_names = ", ".join(action.action for action in result.actions)
        print(f"[{result.priority.value.upper():6}] {result.category.value:10} | {email.subject}")
        print(f"         From: {email.sender} | Actions: {action_names}")
        if result.suggested_response:
            print(f"         Draft: {result.suggested_response}")
    print("\nProcessing complete. No real emails were sent.")


if __name__ == "__main__":
    main()
