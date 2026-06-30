"""
Helper functions - logging, threading, file operations, dll.
"""

import logging
import logging.handlers
from pathlib import Path
from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL
import threading
from functools import wraps
from typing import Callable, Any


def setup_logging(name: str = __name__) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def run_in_thread(func: Callable) -> Callable:
    """
    Decorator untuk run function di thread terpisah.
    
    Usage:
        @run_in_thread
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return wrapper


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if not.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def format_seconds(seconds: float) -> str:
    """
    Format seconds to MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes to human-readable format.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def format_db(level: float) -> str:
    """
    Format level to dB string.
    
    Args:
        level: Linear level (0-1)
        
    Returns:
        dB string
    """
    import math
    if level > 0:
        db = 20 * math.log10(level)
        return f"{db:.2f} dB"
    return "-∞ dB"


class ThreadSafeCounter:
    """Thread-safe counter."""
    
    def __init__(self, initial: int = 0):
        self.value = initial
        self.lock = threading.Lock()
    
    def increment(self) -> int:
        with self.lock:
            self.value += 1
            return self.value
    
    def decrement(self) -> int:
        with self.lock:
            self.value -= 1
            return self.value
    
    def get(self) -> int:
        with self.lock:
            return self.value
