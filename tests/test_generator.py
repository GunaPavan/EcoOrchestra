# tests/test_generator.py

from ecoorchestra.music.generator import create_midi, SoundscapeConfig


def test_create_midi_file():
    config = SoundscapeConfig(
        key_mode="minor",
        tempo_bpm=120,
        instrument="piano",
        density=6,
        bars=4,
        filename="test_output.mid"
    )

    output_path = create_midi(config)

    # ✅ File exists
    assert output_path.exists()

    # ✅ It's a .mid file
    assert output_path.suffix == ".mid"

    # ✅ File has content
    assert output_path.stat().st_size > 100

    # 🧹 Optional cleanup
    # output_path.unlink()
