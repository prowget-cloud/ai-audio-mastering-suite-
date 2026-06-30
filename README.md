````markdown name=README.md
# 🎵 AI Audio Mastering Suite

Aplikasi mastering audio otomatis dengan antarmuka GUI yang user-friendly. Dilengkapi dengan analyzer, quality checker, mastering pipeline, dan report generator.

## ✨ Fitur Utama

- **Audio Analysis**: Analisis metadata dan metrics teknis audio
- **Quality Checking**: Validasi kualitas audio dengan status PASS/WARNING/FAIL
- **Mastering Pipeline**:
  - Normalisasi level
  - Compression dinamis
  - EQ dan effects
  - Limiter untuk prevent clipping
  - Stereo widening
- **Multiple Export**: WAV, MP3, FLAC, OGG
- **Report Generation**: JSON, CSV, dan PDF reports
- **GUI Interface**: Menggunakan CustomTkinter untuk modern UI

## 📋 Struktur Proyek

```
ai-audio-mastering-suite/
├── assets/              # Icon, logo, dll
├── logs/                # File log aplikasi
├── reports/             # Output laporan (PDF/CSV/JSON)
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── gui.py           # CustomTkinter main interface
│   ├── processor.py     # Orchestrator (Worker Thread)
│   ├── analyzer.py      # Audio metadata & technical analysis
│   ├── quality_checker.py # Logic PASS/WARNING/FAIL
│   ├── mastering.py     # Pipeline manager
│   ├── pipeline/        # Komponen individual mastering
│   │   ├── __init__.py
│   │   ├── limiter.py
│   │   ├── normalizer.py
│   │   ├── converter.py
│   │   └── effects.py
│   ├── exporter.py      # File saving logic
│   ├── report_generator.py # PDF/JSON/CSV logic
│   ├── config.py        # Constants, presets, settings
│   └── utils.py         # Helper functions
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Instalasi Dependencies

```bash
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
python src/main.py
```

### Atau langsung dari entry point

```bash
cd src && python main.py
```

## 📖 Dokumentasi Komponen

### Audio Analyzer (`analyzer.py`)
Melakukan analisis komprehensif pada file audio:
- Metadata (filename, format, ukuran file, durasi)
- Teknis (sample rate, channels, bit depth)
- Metrics (RMS level, peak level, dynamic range, crest factor)

```python
from analyzer import AudioAnalyzer

analyzer = AudioAnalyzer()
analysis = analyzer.analyze("input.wav")
print(f"Duration: {analysis['duration']}s")
print(f"RMS Level: {analysis['rms_level']}")
```

### Quality Checker (`quality_checker.py`)
Validasi kualitas audio dengan threshold yang dapat dikonfigurasi:
- Check duration
- Check RMS level
- Check peak level
- Check dynamic range
- Check sample rate

Status: PASS / WARNING / FAIL

```python
from quality_checker import QualityChecker

checker = QualityChecker()
result = checker.check(analysis)
print(f"Status: {result['status']}")
print(f"Checks: {result['checks']}")
```

### Mastering Pipeline
Pipeline yang dapat dikustomisasi untuk proses mastering:

1. **Normalizer** - Normalize ke target RMS level
2. **Effects** - Compression, EQ, stereo widening
3. **Limiter** - Prevent clipping
4. **Converter** - Konversi format dan bit depth

```python
from mastering import MasteringPipeline

pipeline = MasteringPipeline()
mastered = pipeline.process(audio_data, analysis)
```

### Audio Exporter (`exporter.py`)
Export audio ke berbagai format:
- WAV (dengan support untuk berbagai bit depth)
- MP3
- FLAC
- OGG

```python
from exporter import AudioExporter

exporter = AudioExporter()
exporter.export(audio, "output.wav", sample_rate=44100, bit_depth=16)
```

### Report Generator (`report_generator.py`)
Generate comprehensive reports:
- JSON report (lengkap dengan semua data)
- CSV summary
- PDF report (opsional)

```python
from report_generator import ReportGenerator

gen = ReportGenerator()
report = gen.generate(input_file, output_file, analysis, quality)
```

### Audio Processor (`processor.py`)
Orchestrator utama yang mengkoordinasi semua komponen:

```python
from processor import AudioProcessor

processor = AudioProcessor()

# Synchronous processing
result = processor.process("input.wav")

# Asynchronous processing
def callback(success, result_or_error):
    if success:
        print(f"Done! Output: {result_or_error['output_file']}")
    else:
        print(f"Error: {result_or_error}")

processor.process_async("input.wav", callback)
```

## ⚙️ Konfigurasi

Edit `src/config.py` untuk mengubah:
- Audio settings (sample rate, channels, bit depth)
- Mastering presets
- Quality thresholds
- Output paths

Contoh preset:
```python
PRESETS = {
    "balanced": {...},    # Moderate mastering
    "aggressive": {...},  # Heavy processing
    "subtle": {...},      # Minimal processing
}
```

## 📊 Output

### Report Structure

**JSON Report** (`report_YYYYMMDD_HHMMSS.json`):
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "input_file": "/path/to/input.wav",
  "output_file": "/path/to/output.wav",
  "analysis": {
    "filename": "input.wav",
    "duration": 120.5,
    "sample_rate": 44100,
    "rms_level": 0.15,
    "peak_level": 0.95,
    "dynamic_range": 10.5
  },
  "quality": {
    "status": "PASS",
    "checks": [...],
    "warnings": [...],
    "failures": [...]
  }
}
```

**CSV Report** (`report_YYYYMMDD_HHMMSS.csv`):
```
Parameter,Value
Timestamp,2024-01-15T10:30:00
Input File,input.wav
Duration,120.5
RMS Level,0.15
Peak Level,0.95
Status,PASS
```

## 🔧 Troubleshooting

### Error: "Module not found"
Pastikan semua dependencies sudah terinstall:
```bash
pip install -r requirements.txt
```

### Audio tidak terdengar diperkecil
Periksa setting normalization di quality report. RMS level yang terlalu rendah mungkin perlu adjustment.

### Processing lambat
Untuk audio panjang, gunakan asynchronous processing untuk tidak memblok UI:
```python
processor.process_async(input_file, callback)
```

## 📝 Logging

Aplikasi menyimpan logs di `logs/` directory:
- File logs dengan rotation (max 10MB, keep 5 backups)
- Console output untuk development
- Log level dapat diatur di `config.py`

## 🤝 Kontribusi

Silakan fork dan submit pull requests untuk improvements!

## 📄 License

MIT License - Bebas digunakan untuk personal maupun commercial projects.

## 📧 Support

Untuk issues dan questions, silakan buat issue di repository ini.

---

**Made with ❤️ by Prowget Cloud**
````
