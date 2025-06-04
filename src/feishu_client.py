"""Feishu(Lark) API client for document and drive operations."""

import datetime
import json
import requests
from typing import Optional

from . import config


class FeishuClient:
    def __init__(self):
        self._tenant_access_token: Optional[str] = None

    def _get_tenant_access_token(self) -> str:
        """Retrieve tenant access token using app credentials."""
        if self._tenant_access_token:
            return self._tenant_access_token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": config.FEISHU_APP_ID,
            "app_secret": config.FEISHU_APP_SECRET,
        }
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        self._tenant_access_token = data["tenant_access_token"]
        return self._tenant_access_token

    @property
    def headers(self):
        token = self._get_tenant_access_token()
        return {"Authorization": f"Bearer {token}"}

    def _create_doc(self, title: str) -> str:
        """Create a new document and return its token."""
        url = "https://open.feishu.cn/open-apis/doc/v2/create"  # using docs v2
        payload = {
            "title": title,
            "folder_token": config.FEISHU_PARENT_FOLDER_TOKEN,
        }
        resp = requests.post(url, json=payload, headers=self.headers, timeout=5)
        resp.raise_for_status()
        return resp.json()["data"]["document"]["document_id"]

    def _upload_image(self, file_path: str) -> str:
        """Upload image to feishu drive and return the file token."""
        url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
        files = {"file": open(file_path, "rb")}
        data = {
            "file_name": file_path,
            "parent_type": "explorer",
            "parent_node": config.FEISHU_PARENT_FOLDER_TOKEN,
        }
        resp = requests.post(url, headers=self.headers, data=data, files=files, timeout=5)
        resp.raise_for_status()
        return resp.json()["data"]["file_token"]

    def create_or_get_daily_doc(self) -> str:
        """Create or retrieve today's document id."""
        today = datetime.date.today().isoformat()
        title = f"{config.FEISHU_DOC_TITLE_PREFIX}-{today}"
        return self._create_doc(title)

    def append_markdown(self, document_id: str, md: str):
        """Append markdown content to a document."""
        url = f"https://open.feishu.cn/open-apis/doc/v2/{document_id}/batch_update"
        payload = {"requests": [{"insert_block": {"block": {"rich_text": md}, "location": {"index": 0}}}]}
        resp = requests.post(url, json=payload, headers=self.headers, timeout=5)
        resp.raise_for_status()
        return resp.json()

    def upload_image_and_get_link(self, file_path: str) -> str:
        token = self._upload_image(file_path)
        # Feishu docs support linking to drive files using ![](file_token)
        return f"https://open.feishu.cn/file/{token}"
