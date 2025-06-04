"""WeChat listener that forwards incoming messages to a callback."""

from typing import Callable
import itchat
from itchat.content import TEXT, SHARING, PICTURE


class WeChatListener:
    """Listen to WeChat messages using itchat."""

    def __init__(self, message_handler: Callable[[dict], None]):
        """Initialize with a message handler.

        Args:
            message_handler: function to call with message info dict.
        """
        self.message_handler = message_handler

    def start(self):
        """Login and start listening."""
        # QR code login. hotReload allows auto relogin without rescanning.
        itchat.auto_login(hotReload=True)

        @itchat.msg_register([TEXT, SHARING, PICTURE], isFriendChat=True, isGroupChat=True)
        def _(msg):
            info = {
                "type": msg.type,
                "text": msg.text,
                "file_name": msg.fileName if hasattr(msg, "fileName") else None,
            }
            if msg.type == 'Picture':
                # Download image file locally; path returned by itchat
                info["file_path"] = msg.download(msg.fileName)
            elif msg.type == 'Sharing':
                info["url"] = msg.url
            self.message_handler(info)

        itchat.run(blockThread=True)
