# ASR Studio — Automatic Speech Recognition Tool

A local web application that converts uploaded audio into text using **faster-whisper**, an optimized implementation of OpenAI Whisper. It supports language selection, timestamped segments, and SRT subtitle export.

## Features

- Upload WAV, MP3, M4A, FLAC, OGG, MP4, and WebM audio/media files.
- Automatic language detection or manually select a supported language.
- Choose Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`).
- View and download plain-text transcripts.
- View segment timestamps and export subtitles as `.srt`.
- CPU-friendly inference using int8 quantization.
- Unit tests that run without downloading model weights.

## Technologies used

- **Python 3.10+** — application logic
- **Streamlit** — web UI
- **faster-whisper** — automatic speech recognition
- **CTranslate2** — optimized inference backend used by faster-whisper
- **pytest** — automated unit tests
- **Git and GitHub** — version control and project hosting

## Project structure

```text
asr-tool/
├── app.py
├── asr_tool/
│   ├── __init__.py
│   └── transcriber.py
├── tests/
│   └── test_transcriber.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- Internet access for installing dependencies and downloading a model the first time
- Enough RAM and disk space for the selected model; `tiny` or `base` is recommended for initial testing
- CPU is supported. GPU acceleration depends on a compatible CUDA/CTranslate2 setup.

## Run locally

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`), upload an audio file, choose settings, and click **Transcribe audio**. The first transcription may take longer while model files are downloaded.

## Run tests

The tests use a fake model, so they do not need an audio sample, a model download, or a GPU.

```bash
pytest -q
```

Expected result: **4 passed**.

## Upload to GitHub

Create an empty repository on GitHub (for example, `asr-tool`). Then run these commands from this project folder:

```bash
git init
git add .
git commit -m "Build ASR Studio speech recognition tool"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/asr-tool.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. If the repository already exists locally, add the files to that repository instead of running `git init` again. Never commit access tokens or credentials.

## Notes and limitations

- Speech recognition quality depends on audio clarity, accents, background noise, and model size.
- Larger models generally improve recognition but use more memory and run more slowly.
- This app processes audio locally after dependencies and model weights are available; the first model download requires internet access.
- Do not upload private or sensitive recordings unless you have permission to process them.
- The tests validate the transcription wrapper and subtitle formatting. They do not measure real-world word error rate; evaluate with representative audio before production use.

## License

Choose a license appropriate for your intended use before publishing. The faster-whisper project and its dependencies have their own licenses.
