"""Speech-to-text helpers powered by faster-whisper."""
from __future__ import annotations

from typing import Any


def load_model(model_size: str = "base", device: str = "cpu"):
    """Load a Whisper model. Import lazily so formatting/tests work without the model installed."""
    from faster_whisper import WhisperModel

    return WhisperModel(model_size, device=device, compute_type="int8" if device == "cpu" else "float16")


def transcribe_audio(
    audio_path: str,
    model_size: str = "base",
    language: str | None = None,
    device: str = "cpu",
    model: Any | None = None,
) -> dict[str, Any]:
    """Transcribe an audio file and return plain text, segments, and detected language.

    Pass a model object to avoid loading weights in tests or when reusing a loaded model.
    """
    if model is None:
        model = load_model(model_size=model_size, device=device)
    segments_iter, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True,
    )
    segments = [
        {"start": float(segment.start), "end": float(segment.end), "text": str(segment.text)}
        for segment in segments_iter
    ]
    return {
        "text": " ".join(segment["text"].strip() for segment in segments).strip(),
        "segments": segments,
        "language": getattr(info, "language", language),
    }


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS,mmm for subtitle timestamps."""
    milliseconds = max(0, round(float(seconds) * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def format_srt(segments: list[dict[str, Any]]) -> str:
    """Convert transcript segments to SubRip (SRT) subtitle text."""
    blocks = []
    for index, segment in enumerate(segments, start=1):
        blocks.append(
            f"{index}\n{format_timestamp(segment['start'])} --> "
            f"{format_timestamp(segment['end'])}\n{segment['text'].strip()}"
        )
    return "\n\n".join(blocks) + ("\n" if blocks else "")
