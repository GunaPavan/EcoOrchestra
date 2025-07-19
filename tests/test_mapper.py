from ecoorchestra.music.mapper import map_env_to_music, MusicParameters


def test_map_env_to_music():
    mapped = map_env_to_music(temp=35.5, humidity=37, wind=4.3, aqi=77)

    assert isinstance(mapped, MusicParameters)

    assert mapped.key_mode in ("major", "minor")
    assert 60 <= mapped.tempo_bpm <= 180
    assert mapped.instrument in ("piano", "synth_bass", "ambient_pad")
    assert 2 <= mapped.density <= 12
