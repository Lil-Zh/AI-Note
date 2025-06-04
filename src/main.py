"""Entry point for the AI WeChat assistant."""

from .note_manager import NoteManager
from .wechat_listener import WeChatListener


def main():
    manager = NoteManager()
    listener = WeChatListener(manager.handle_message)
    listener.start()


if __name__ == "__main__":
    main()
