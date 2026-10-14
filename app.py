import tempfile
from pathlib import Path

import streamlit as st

from asr_tool.transcriber import transcribe_audio, format_srt, format_timestamp

st.set_page_config(page_title="ASR Studio", page_icon="🎙️", layout="wide")
st.title("🎙️ ASR Studio")
st.write("Transcribe audio files into readable text with optional timestamps and subtitle export.")

with st.sidebar:
    st.header("Transcription settings")
    model_size = st.selectbox("Whisper model", ["tiny", "base", "small", "medium", "large-v3"], index=1)
    language_choice = st.selectbox("Audio language", ["Auto-detect", "English", "Tamil", "Hindi", "Spanish", "French", "German", "Japanese"])
    language_codes = {
        "English": "en", "Tamil": "ta", "Hindi": "hi", "Spanish": "es",
        "French": "fr", "German": "de", "Japanese": "ja"
    }
    language = language_codes.get(language_choice)
    device = st.selectbox("Device", ["cpu"], index=0)
    st.caption("The first run may download model files. Larger models are slower and need more memory.")

audio = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a", "flac", "ogg", "mpeg", "mp4", "webm"])
if audio:
    st.audio(audio)
    if st.button("Transcribe audio", type="primary"):
        suffix = Path(audio.name).suffix or ".audio"
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(audio.getbuffer())
                tmp_path = tmp.name
            with st.spinner("Transcribing… this can take a while for large files/models."):
                result = transcribe_audio(tmp_path, model_size=model_size, language=language, device=device)
            st.success("Transcription completed.")
            st.subheader("Transcript")
            transcript = result["text"].strip()
            st.text_area("Recognized speech", transcript, height=260)
            st.download_button("Download transcript (.txt)", transcript, file_name="transcript.txt", mime="text/plain")
            if result["segments"]:
                st.subheader("Segments and timestamps")
                st.dataframe(
                    [{"Start": format_timestamp(s["start"]), "End": format_timestamp(s["end"]), "Text": s["text"].strip()}
                     for s in result["segments"]],
                    use_container_width=True
                )
                st.download_button("Download subtitles (.srt)", format_srt(result["segments"]),
                                   file_name="transcript.srt", mime="application/x-subrip")
            st.caption(f"Detected language: {result.get('language') or 'unknown'}")
        except Exception as exc:
            st.error(f"Transcription failed: {exc}")
            st.info("Check that the audio file is valid and that dependencies/model downloads are available.")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
else:
    st.info("Choose an audio file above to begin.")
