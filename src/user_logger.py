import logging
import os
from datetime import datetime

_LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(_LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(_LOG_DIR, "user_actions.log")

_file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
_file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)

_action_logger = logging.getLogger("user_actions")
_action_logger.setLevel(logging.INFO)
_action_logger.addHandler(_file_handler)
_action_logger.propagate = True


def log_action(username: str, action: str) -> None:
    
    _action_logger.info(f"USER={username!r} | {action}")


def get_log_path() -> str:
   
    return os.path.abspath(_LOG_FILE)
