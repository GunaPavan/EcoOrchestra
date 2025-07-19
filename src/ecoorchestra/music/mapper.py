from dataclasses import dataclass


@dataclass
class MusicParameters:
    key_mode: str         # "major" or "minor"
    tempo_bpm: int        # 60–180 BPM
    instrument: str       # "piano", "synth_bass", "ambient_pad"
    density: int          # rhythmic density, 2–12 notes


def map_env_to_music(temp: float, humidity: float, wind: float, aqi: int) -> MusicParameters:
    """
    Maps environmental data to musical parameters.

    Parameters:
    - temp: Temperature in Celsius
    - humidity: Percentage (0–100)
    - wind: Wind speed in m/s
    - aqi: Air Quality Index (0–500)

    Returns:
    - MusicParameters dataclass with mapped values
    """

    # 🎵 Key Mode
    key_mode = "major" if aqi < 100 else "minor"

    # 🕒 Tempo (scale 60–180 bpm)
    temp = max(min(temp, 60), -10)  # clamp temp to avoid extremes
    tempo_bpm = int(60 + (temp * 2))
    tempo_bpm = min(max(tempo_bpm, 60), 180)

    # 🎹 Instrument Selection
    if humidity < 30:
        instrument = "synth_bass"
    elif humidity < 60:
        instrument = "piano"
    else:
        instrument = "ambient_pad"

    # 🎶 Rhythmic Complexity (scale 2–12)
    wind = max(wind, 0)
    density = min(max(int(wind * 2), 2), 12)

    return MusicParameters(
        key_mode=key_mode,
        tempo_bpm=tempo_bpm,
        instrument=instrument,
        density=density
    )
