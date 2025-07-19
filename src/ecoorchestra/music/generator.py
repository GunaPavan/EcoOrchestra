# src/ecoorchestra/music/generator.py

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from dataclasses import dataclass
from pathlib import Path
import random

DEFAULT_OUTPUT_DIR = Path("output")
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INSTRUMENT_PROGRAMS = {
    "piano": 0,
    "synth_bass": 38,
    "ambient_pad": 89
}

SCALE_MODES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10]
}


@dataclass
class SoundscapeConfig:
    key_mode: str = "major"
    tempo_bpm: int = 90
    instrument: str = "piano"
    density: int = 4        # notes per bar
    bars: int = 4
    filename: str = "soundscape.mid"


def create_midi(config: SoundscapeConfig) -> Path:
    """
    Generate a MIDI file based on the given soundscape configuration.
    Returns the path to the saved MIDI file.
    """
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # 🎹 Instrument program
    program_number = INSTRUMENT_PROGRAMS.get(config.instrument, 0)
    track.append(Message("program_change", program=program_number, time=0))

    # 🕒 Tempo
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(config.tempo_bpm)))

    # 🎼 Melody
    base_note = 60  # Middle C
    scale = SCALE_MODES.get(config.key_mode, SCALE_MODES["major"])
    note_length = 480  # 1 beat in MIDI ticks

    total_notes = config.density * config.bars
    for _ in range(total_notes):
        note = base_note + random.choice(scale)
        velocity = random.randint(60, 100)
        track.append(Message("note_on", note=note, velocity=velocity, time=0))
        track.append(Message("note_off", note=note, velocity=velocity, time=note_length))

    output_path = DEFAULT_OUTPUT_DIR / config.filename
    midi.save(str(output_path))

    return output_path
