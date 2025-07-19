# src/ecoorchestra/pipeline/main_pipeline.py
from datetime import datetime
import json
from pathlib import Path

from ecoorchestra.data.fetcher import get_weather_data, get_aqi_data
from ecoorchestra.music.mapper import map_env_to_music
from ecoorchestra.music.generator import SoundscapeConfig, create_midi
from ecoorchestra.audio.renderer import midi_to_wav

def run_pipeline(city="Delhi", state="Delhi", country="India", save_metadata=True):
    print("🚀 Running EcoOrchestra pipeline...")

    # Step 1: Fetch environmental data
    weather = get_weather_data(city, country)
    aqi = get_aqi_data(city, state, country)

    if weather is None or aqi is None:
        print("❌ Failed to retrieve environment data. Aborting.")
        return

    print("🌡️ Weather:", weather)
    print("🌫️ AQI:", aqi)

    # Step 2: Map to musical parameters
    music_params = map_env_to_music(
        temp=weather.temperature,
        humidity=weather.humidity,
        wind=weather.wind_speed,
        aqi=aqi.aqi
    )
    print("🎼 Mapped Music Parameters:", music_params)

    # Step 3: File naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    midi_filename = f"eco_{timestamp}.mid"
    wav_filename = f"eco_{timestamp}.wav"
    midi_path = Path("output") / midi_filename
    wav_path = Path("output") / wav_filename
    sf2_path = Path("assets") / "FluidR3_GM.sf2"

    # Step 4: Generate MIDI
    midi_file = create_midi(SoundscapeConfig(
        key_mode=music_params.key_mode,
        tempo_bpm=music_params.tempo_bpm,
        instrument=music_params.instrument,
        density=music_params.density,
        filename=midi_filename
    ))
    print(f"🎹 MIDI created at: {midi_file}")

    # Step 5: Convert to WAV
    midi_to_wav(midi_file, sf2_path, wav_path)
    print(f"🔊 WAV created at: {wav_path}")

    # Step 6: Save metadata
    if save_metadata:
        metadata = {
            "timestamp": timestamp,
            "city": city,
            "environment": {
                "temperature": weather.temperature,
                "humidity": weather.humidity,
                "wind_speed": weather.wind_speed,
                "aqi": aqi.aqi
            },
            "music_parameters": music_params.__dict__,
            "midi_file": str(midi_path),
            "wav_file": str(wav_path)
        }
        metadata_path = Path("output") / f"eco_{timestamp}.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"📝 Metadata saved at: {metadata_path}")

    print("✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
