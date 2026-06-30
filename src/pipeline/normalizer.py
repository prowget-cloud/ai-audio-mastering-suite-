"""
Normalizer effect - normalize audio level ke target RMS.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)


class Normalizer:
    """Normalizer untuk normalize audio level."""
    
    def __init__(self, target_rms: float = 0.15):
        """
        Initialize Normalizer.
        
        Args:
            target_rms: Target RMS level (0-1)
        """
        self.target_rms = target_rms
    
    def normalize(self, audio: np.ndarray, peak_normalization: bool = False) -> np.ndarray:
        """
        Normalize audio level.
        
        Args:
            audio: Input audio array
            peak_normalization: Use peak normalization instead of RMS
            
        Returns:
            Normalized audio
        """
        logger.info(f"Normalizing audio to RMS {self.target_rms}")
        
        if peak_normalization:
            # Normalize ke peak
            peak = np.max(np.abs(audio))
            if peak > 0:
                output = audio / peak * 0.95
        else:
            # Normalize ke RMS
            rms = np.sqrt(np.mean(audio ** 2))
            if rms > 0:
                output = audio * (self.target_rms / rms)
            else:
                output = audio
        
        return output
