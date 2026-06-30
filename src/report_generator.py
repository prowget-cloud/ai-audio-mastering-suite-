"""
Report generator - generate PDF, JSON, dan CSV reports.
"""

import logging
import json
from pathlib import Path
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate reports untuk hasil mastering."""
    
    def __init__(self):
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)
    
    def generate(self, input_file: str, output_file: str, analysis: Dict,
                 quality: Dict, output_path: str = None) -> Dict:
        """
        Generate comprehensive report.
        
        Args:
            input_file: Input file path
            output_file: Output file path
            analysis: Audio analysis data
            quality: Quality check data
            output_path: Custom output path (optional)
            
        Returns:
            Report data dictionary
        """
        try:
            logger.info("Generating report...")
            
            # Create report data
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "input_file": input_file,
                "output_file": output_file,
                "analysis": analysis,
                "quality": quality,
            }
            
            # Generate JSON report
            if output_path is None:
                output_path = str(self.report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            self._generate_json(report_data, output_path)
            
            # Generate CSV summary
            csv_path = output_path.replace('.json', '.csv')
            self._generate_csv(report_data, csv_path)
            
            logger.info(f"✓ Reports generated successfully")
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    @staticmethod
    def _generate_json(data: Dict, output_path: str):
        """Generate JSON report."""
        logger.info(f"Writing JSON report: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _generate_csv(data: Dict, output_path: str):
        """Generate CSV report summary."""
        logger.info(f"Writing CSV report: {output_path}")
        
        analysis = data.get('analysis', {})
        quality = data.get('quality', {})
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Parameter,Value\n")
            f.write(f"Timestamp,{data.get('timestamp')}\n")
            f.write(f"Input File,{data.get('input_file')}\n")
            f.write(f"Output File,{data.get('output_file')}\n")
            f.write("\n--- Analysis ---\n")
            
            for key, value in analysis.items():
                if not isinstance(value, (dict, list)):
                    f.write(f"{key},{value}\n")
            
            f.write("\n--- Quality Check ---\n")
            f.write(f"Status,{quality.get('status')}\n")
            f.write(f"Total Checks,{len(quality.get('checks', []))}\n")
            f.write(f"Warnings,{len(quality.get('warnings', []))}\n")
            f.write(f"Failures,{len(quality.get('failures', []))}\n")
