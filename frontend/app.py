import io
import sys
from datetime import datetime
from pathlib import Path
import streamlit as st
from ecoorchestra.data.fetcher import fetch_environment_data
from ecoorchestra.music.env_to_prompt import map_env_to_prompt
from ecoorchestra.music.musicgen_infer import generate_music_from_prompt

# --- Path Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Ensure output folder exists
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    st.set_page_config(page_title="EcoOrchestra", layout="centered")
    st.title("🌿 EcoOrchestra AI Music Generator")

    # Initialize session state
    if 'audio_bytes' not in st.session_state:
        st.session_state.audio_bytes = None
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    if 'temp_file' not in st.session_state:  # Store saved file path
        st.session_state.temp_file = None

    # User Input Form
    with st.form(key="music_form"):
        cols = st.columns(3)
        city = cols[0].text_input("City", placeholder="e.g. Tokyo")
        state = cols[1].text_input("State/Region", placeholder="e.g. Kanto")
        country = cols[2].text_input("Country", placeholder="e.g. Japan")

        if st.form_submit_button("Generate Music", type="primary"):
            if not all([city.strip(), state.strip(), country.strip()]):
                st.error("All fields are required!")
                st.stop()

            try:
                with st.status("Generating music...", expanded=True):
                    # 1. Get environmental data
                    st.write("🌍 Fetching environmental data...")
                    env_data = fetch_environment_data(city, state, country)

                    # 2. Create music prompt
                    st.write("🎵 Creating music prompt...")
                    prompt = map_env_to_prompt(**env_data)

                    # 3. Generate audio (in memory)
                    st.write("🎶 Composing music...")
                    audio_bytes = io.BytesIO()
                    generate_music_from_prompt(prompt, audio_bytes)
                    st.session_state.audio_bytes = audio_bytes
                    st.session_state.generated = True

                    # 4. Save to output folder
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    temp_path = OUTPUT_DIR / f"eco_music_{timestamp}.wav"
                    with open(temp_path, "wb") as f:
                        f.write(audio_bytes.getbuffer())
                    st.session_state.temp_file = temp_path

                    st.success("✅ Music generated successfully!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    # Display results outside the form
    if st.session_state.generated and st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format="audio/wav")

        # Download Option
        col1, _ = st.columns(2)
        col1.download_button(
            "Download Locally",
            data=st.session_state.audio_bytes,
            file_name=f"eco_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
            mime="audio/wav",
            type="primary"
        )


if __name__ == "__main__":
    main()
