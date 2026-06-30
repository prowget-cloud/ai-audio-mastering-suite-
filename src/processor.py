"""
Orchestrator untuk proses mastering audio.
Mengelola worker thread dan koordinasi komponen.
"""

import threading
import logging
from pathlib import Path
from analyzer import AudioAnalyzer
from quality_checker import QualityChecker
from mastering import MasteringPipeline
from exporter import AudioExporter
from report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Orchestrator untuk proses audio mastering."""
    
    def __init__(self):
        self.analyzer = AudioAnalyzer()
        self.quality_checker = QualityChecker()
        self.mastering = MasteringPipeline()
        self.exporter = AudioExporter()
        self.report_gen = ReportGenerator()
        
    def process(self, input_file: str, output_file: str = None):
        """
        Proses audio file secara lengkap.
        
        Args:
            input_file: Path ke file audio input
            output_file: Path untuk output (opsional)
        """
        try:
            input_path = Path(input_file)
            
            if not input_path.exists():
                raise FileNotFoundError(f"File tidak ditemukan: {input_file}")
            
            logger.info(f"Memulai processing: {input_file}")
            
            # 1. Analyze audio
            logger.info("Step 1: Analisis audio...")
            analysis = self.analyzer.analyze(input_file)
            logger.info(f"Durasi: {analysis['duration']}s, Sample rate: {analysis['sample_rate']}Hz")
            
            # 2. Check quality
            logger.info("Step 2: Pengecekan kualitas...")
            quality = self.quality_checker.check(analysis)
            logger.info(f"Status: {quality['status']}")
            
            # 3. Apply mastering
            logger.info("Step 3: Proses mastering...")
            audio_data = self.analyzer.load_audio(input_file)
            mastered = self.mastering.process(audio_data, analysis)
            
            # 4. Export
            if output_file is None:
                output_file = str(input_path.parent / f"{input_path.stem}_mastered.wav")
            
            logger.info(f"Step 4: Export ke {output_file}...")
            self.exporter.export(mastered, output_file, analysis['sample_rate'])
            
            # 5. Generate report
            logger.info("Step 5: Generate laporan...")
            report_path = str(input_path.parent / f"{input_path.stem}_report.json")
            self.report_gen.generate(
                input_file,
                output_file,
                analysis,
                quality,
                report_path
            )
            
            logger.info("✓ Proses mastering selesai!")
            return {
                "output_file": output_file,
                "report_file": report_path,
                "analysis": analysis,
                "quality": quality
            }
            
        except Exception as e:
            logger.error(f"Error dalam processing: {e}", exc_info=True)
            raise
    
    def process_async(self, input_file: str, callback=None):
        """
        Proses audio secara asynchronous di thread terpisah.
        
        Args:
            input_file: Path ke file audio
            callback: Function untuk dipanggil setelah selesai
        """
        def worker():
            try:
                result = self.process(input_file)
                if callback:
                    callback(True, result)
            except Exception as e:
                if callback:
                    callback(False, str(e))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread
