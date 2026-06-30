"""
Converter - konversi format audio dan bit depth.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)


class Converter:
    """Converter untuk convert format dan bit depth audio."""
    
    SUPPORTED_FORMATS = ['int16', 'int24', 'int32', 'float32', 'float64']
    SUPPORTED_SAMPLE_RATES = [22050, 44100, 48000, 96000, 192000]
    
    def convert(self, audio: np.ndarray, target_format: str = 'int16',
                target_sample_rate: int = None) -> np.ndarray:
        """
        Convert audio format dan/atau sample rate.
        
        Args:
            audio: Input audio array
            target_format: Target format (int16, float32, dll)
            target_sample_rate: Target sample rate (opsional)
            
        Returns:
            Converted audio
        """
        if target_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {target_format}")
        
        logger.info(f"Converting audio to {target_format}")
        
        # Convert format
        output = self._convert_format(audio, target_format)
        
        # Resample if needed
        if target_sample_rate and target_sample_rate != 44100:  # Assume input is 44.1kHz
            logger.info(f"Resampling to {target_sample_rate} Hz")
            # Placeholder - implementasi nyata menggunakan librosa atau scipy
            pass
        
        return output
    
    @staticmethod
    def _convert_format(audio: np.ndarray, target_format: str) -> np.ndarray:
        """Convert audio format."""
        if target_format == 'int16':
            # Normalize ke int16 range
            audio = np.clip(audio, -1.0, 1.0)
            return (audio * 32767).astype(np.int16)
        
        elif target_format == 'int24':
            audio = np.clip(audio, -1.0, 1.0)
            return (audio * 8388607).astype(np.int32)
        
        elif target_format == 'int32':
            audio = np.clip(audio, -1.0, 1.0)
            return (audio * 2147483647).astype(np.int32)
        
        elif target_format == 'float32':
            return audio.astype(np.float32)
        
        elif target_format == 'float64':
            return audio.astype(np.float64)
        
        return audio
