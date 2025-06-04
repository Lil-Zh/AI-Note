#!/bin/bash
# Deployment script for the AI WeChat assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install itchat requests

# Run the assistant
python -m src.main
