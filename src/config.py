"""
Configuration constants, presets, dan settings.
"""

from pathlib import Path
import os

# Application info
APP_NAME = "AI Audio Mastering Suite"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories if not exist
for dir_path in [ASSETS_DIR, LOGS_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Audio settings
SAMPLE_RATE = 44100
CHANNELS = 2
BIT_DEPTH = 16

# Mastering presets
PRESETS = {
    "balanced": {
        "normalize": True,
        "compression_ratio": 4.0,
        "eq_enabled": True,
        "limiter_threshold": 0.95,
        "stereo_width": 1.0,
    },
    "aggressive": {
        "normalize": True,
        "compression_ratio": 6.0,
        "eq_enabled": True,
        "limiter_threshold": 0.92,
        "stereo_width": 1.3,
    },
    "subtle": {
        "normalize": True,
        "compression_ratio": 2.0,
        "eq_enabled": False,
        "limiter_threshold": 0.98,
        "stereo_width": 0.8,
    },
}

# Quality thresholds
QUALITY_THRESHOLDS = {
    "min_duration": 5,  # seconds
    "min_sample_rate": 44100,  # Hz
    "ideal_rms": 0.15,  # -16.5 dBFS
    "ideal_peak": 0.95,  # -0.4 dBFS
    "ideal_dr_range": (8, 14),  # Dynamic range
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / f"{APP_NAME.lower().replace(' ', '_')}.log"

# Supported formats
SUPPORTED_INPUT_FORMATS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
SUPPORTED_OUTPUT_FORMATS = ['.wav', '.mp3', '.flac']
