import os
import sys

# Compute project root explicitly from file location
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

for path in [root_dir, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from src.main import app

# Expose app for ASGI / Vercel Serverless Function
handler = app
