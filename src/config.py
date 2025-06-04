"""Configuration placeholders for the assistant."""

# Feishu (Lark) App credentials
FEISHU_APP_ID = "YOUR_APP_ID"
FEISHU_APP_SECRET = "YOUR_APP_SECRET"

# WeChat login settings (itchat uses QR scan by default)
# If using WeChaty, add your token here
WECHAT_TOKEN = "YOUR_WECHAT_TOKEN"

# Storage options
FEISHU_DOC_TITLE_PREFIX = "随手记"
FEISHU_PARENT_FOLDER_TOKEN = "FOLDER_TOKEN"  # Where docs and images will be saved

# Default mode: create a daily document
DAILY_DOC = True
