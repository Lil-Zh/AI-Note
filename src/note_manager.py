"""Handle message classification and persistence to Feishu."""

import re
from datetime import datetime
from typing import Dict

from .feishu_client import FeishuClient
from . import config


class NoteManager:
    def __init__(self):
        self.feishu = FeishuClient()
        if config.DAILY_DOC:
            self.doc_id = self.feishu.create_or_get_daily_doc()
        else:
            self.doc_id = self.feishu._create_doc(config.FEISHU_DOC_TITLE_PREFIX)

    def _classify(self, info: Dict) -> str:
        """Return category name for the message."""
        text = info.get("text", "")
        if info.get("type") == "Sharing" or re.search(r"https?://", text):
            return "link"
        if "#TODO" in text:
            return "todo"
        if "灵感" in text or "#idea" in text:
            return "idea"
        if info.get("type") == "Picture":
            return "image"
        return "other"

    def handle_message(self, info: Dict):
        category = self._classify(info)
        now = datetime.now().strftime("%H:%M")
        if category == "link":
            md = f"- [链接]({info.get('url') or info.get('text')}) {now}\n"
        elif category == "todo":
            md = f"- [ ] {info['text']} {now}\n"
        elif category == "idea":
            md = f"- 💡 {info['text']} {now}\n"
        elif category == "image":
            link = self.feishu.upload_image_and_get_link(info['file_path'])
            md = f"![image]({link}) {now}\n"
        else:
            md = f"- {info['text']} {now}\n"

        self.feishu.append_markdown(self.doc_id, md)
