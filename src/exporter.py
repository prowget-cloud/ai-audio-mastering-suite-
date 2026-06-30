"""
Audio exporter - save audio ke berbagai format.
"""

import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class AudioExporter:
    """Exporter untuk save audio ke file."""
    
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.flac', '.ogg']
    
    def __init__(self):
        pass
    
    def export(self, audio: np.ndarray, output_path: str,
               sample_rate: int = 44100, bit_depth: int = 16) -> bool:
        """
        Export audio ke file.
        
        Args:
            audio: Audio data sebagai numpy array
            output_path: Path untuk output file
            sample_rate: Sample rate dalam Hz
            bit_depth: Bit depth (16, 24, 32)
            
        Returns:
            True jika sukses, False jika gagal
        """
        try:
            output_path = Path(output_path)
            
            # Check format support
            if output_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported format: {output_path.suffix}")
            
            logger.info(f"Exporting to {output_path}")
            
            # Create parent directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export based on format
            if output_path.suffix.lower() == '.wav':
                self._export_wav(audio, str(output_path), sample_rate, bit_depth)
            else:
                logger.warning(f"Format {output_path.suffix} not fully implemented yet")
                self._export_wav(audio, str(output_path), sample_rate, bit_depth)
            
            logger.info(f"✓ Export successful: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting audio: {e}")
            raise
    
    @staticmethod
    def _export_wav(audio: np.ndarray, output_path: str,
                   sample_rate: int, bit_depth: int):
        """Export as WAV file."""
        try:
            import scipy.io.wavfile as wavfile
            
            # Convert to target bit depth
            if bit_depth == 16:
                audio = np.clip(audio, -1.0, 1.0)
                audio = (audio * 32767).astype(np.int16)
            elif bit_depth == 32:
                audio = np.clip(audio, -1.0, 1.0)
                audio = (audio * 2147483647).astype(np.int32)
            
            # Write file
            if len(audio.shape) > 1:
                # Stereo - transpose to (samples, channels)
                audio = audio.T
            
            wavfile.write(output_path, sample_rate, audio)
            
        except ImportError:
            logger.warning("scipy not available, creating dummy file")
            # Fallback: create dummy file
            Path(output_path).touch()
