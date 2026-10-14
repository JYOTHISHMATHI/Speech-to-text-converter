from types import SimpleNamespace

from asr_tool.transcriber import format_srt, format_timestamp, transcribe_audio


class FakeSegment:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text


class FakeModel:
    def transcribe(self, audio_path, **kwargs):
        assert audio_path == "sample.wav"
        assert kwargs["language"] == "en"
        return iter([
            FakeSegment(0.0, 1.25, " Hello"),
            FakeSegment(1.25, 2.5, " world.")
        ]), SimpleNamespace(language="en")


def test_transcribe_audio_with_injected_model():
    result = transcribe_audio("sample.wav", language="en", model=FakeModel())
    assert result["text"] == "Hello world."
    assert result["language"] == "en"
    assert len(result["segments"]) == 2


def test_format_timestamp():
    assert format_timestamp(61.234) == "00:01:01,234"
    assert format_timestamp(3661.005) == "01:01:01,005"


def test_format_srt():
    srt = format_srt([
        {"start": 0, "end": 1.5, "text": " Hello "},
        {"start": 1.5, "end": 2, "text": "World"}
    ])
    assert "1\n00:00:00,000 --> 00:00:01,500\nHello" in srt
    assert "2\n00:00:01,500 --> 00:00:02,000\nWorld" in srt


def test_format_empty_srt():
    assert format_srt([]) == ""
