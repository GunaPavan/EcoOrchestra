import subprocess
from pathlib import Path


def midi_to_wav(midi_path: str, sf2_path: str, wav_path: str) -> None:
    """
    Converts a MIDI file to WAV using FluidSynth CLI.

    Parameters:
        midi_path (str): Path to the input MIDI file.
        sf2_path (str): Path to the SoundFont (.sf2) file.
        wav_path (str): Desired output path for the WAV file.

    Raises:
        FileNotFoundError: If input files are missing.
        RuntimeError: If FluidSynth fails or output is invalid.
    """

    # 📁 Normalize absolute paths
    midi_path = Path(midi_path).resolve()
    sf2_path = Path(sf2_path).resolve()
    wav_path = Path(wav_path).resolve()

    print("🔍 Verifying input files...")
    if not midi_path.exists():
        raise FileNotFoundError(f"❌ MIDI file not found: {midi_path}")
    if not sf2_path.exists():
        raise FileNotFoundError(f"❌ SoundFont file not found: {sf2_path}")

    print(f"🎵 MIDI file:     {midi_path}")
    print(f"🎹 SoundFont:     {sf2_path}")
    print(f"🔊 Output (WAV):  {wav_path}")

    # 🛠️ Build FluidSynth CLI command
    command = [
        "fluidsynth",
        "-ni",                        # No shell, interactive off
        "-F", str(wav_path),          # Output file
        "-T", "wav",                  # Output type
        "-r", "44100",                # Sample rate
        str(sf2_path),
        str(midi_path),
    ]

    print("🚀 Running FluidSynth...")
    print("🧪 Command:\n", " ".join(command))

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("⏳ Conversion timed out. Check MIDI length or system performance.")

    print("📤 STDOUT:\n", result.stdout.strip())
    print("📥 STDERR:\n", result.stderr.strip())
    print("📟 Exit Code:", result.returncode)

    if result.returncode != 0:
        raise RuntimeError("❌ FluidSynth failed to convert MIDI to WAV.")

    if not wav_path.exists() or wav_path.stat().st_size == 0:
        raise RuntimeError("⚠️ WAV file was not created or is empty.")

    print(f"✅ WAV file created successfully: {wav_path}")
