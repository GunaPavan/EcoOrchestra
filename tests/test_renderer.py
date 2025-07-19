from pathlib import Path
from ecoorchestra.audio.renderer import midi_to_wav
from ecoorchestra.music.generator import create_midi


def test_midi_to_wav_conversion():
    print("✅ Running renderer test...")

    # Define paths
    output_dir = Path("output")
    assets_dir = Path("assets")
    midi_path = output_dir / "test_output.mid"
    wav_path = output_dir / "test_output.wav"
    sf2_path = assets_dir / "FluidR3_GM.sf2"

    # Ensure required folders exist
    output_dir.mkdir(exist_ok=True)
    assets_dir.mkdir(exist_ok=True)

    # Check SoundFont presence
    assert sf2_path.exists(), (
        f"❌ SoundFont file not found: {sf2_path}\n"
        f"💡 Place a .sf2 file (e.g. FluidR3_GM.sf2) in the 'assets/' directory."
    )

    # Auto-create MIDI if missing
    if not midi_path.exists():
        print("🎹 MIDI not found. Creating via create_midi()...")
        create_midi(
            key_mode="minor",
            tempo=120,
            instrument="piano",
            density=6,
            filename=midi_path.name  # pass only filename
        )

    assert midi_path.exists(), f"❌ MIDI file not created at: {midi_path}"

    print("🎼 Converting MIDI to WAV...")
    midi_to_wav(str(midi_path), str(sf2_path), str(wav_path))

    assert wav_path.exists(), f"❌ WAV file not created at: {wav_path}"
    assert wav_path.stat().st_size > 0, "❌ WAV file is empty"

    print("✅ WAV file conversion successful!")
