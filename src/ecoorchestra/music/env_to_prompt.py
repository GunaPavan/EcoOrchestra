# src/ecoorchestra/music/env_to_prompt.py

def map_env_to_prompt(
    temperature: float,
    humidity: float,
    wind_speed: float,
    aqi: int
) -> str:
    """
    Maps environmental parameters to a natural language prompt for MusicGen.
    Produces emotionally resonant music reflecting real-time climate conditions.
    """

    mood = "ambient"
    descriptors = []
    instrument = "piano"
    tone = ""

    # 🌡️ Temperature logic
    if temperature >= 40:
        mood = "intense"
        descriptors.append("sweltering heat")
        instrument = "synths"
    elif temperature >= 30:
        descriptors.append("warm breeze")
    elif temperature <= 10:
        mood = "cold and slow"
        descriptors.append("frosty air")
        instrument = "strings"
    else:
        descriptors.append("mild climate")

    # 💧 Humidity logic
    if humidity > 85:
        descriptors.append("dense humidity")
        tone = "uneasy and heavy"
    elif humidity > 70:
        descriptors.append("sticky atmosphere")
    elif humidity < 30:
        descriptors.append("dry winds")
        tone = "crisp and sharp"

    # 🌬️ Wind logic
    if wind_speed > 20:
        mood = "stormy"
        descriptors.append("howling gusts")
        instrument = "brass"
    elif wind_speed > 12:
        mood = "chaotic"
        descriptors.append("strong breeze")
        instrument = "percussion-heavy"
    elif wind_speed > 6:
        descriptors.append("light breeze")
    else:
        descriptors.append("calm air")

    # 🌫️ Air Quality Index (AQI)
    if aqi > 300:
        tone = "apocalyptic"
        instrument = "distorted synthesizers"
        descriptors.append("toxic smog")
    elif aqi > 200:
        tone = "dystopian"
        instrument = "distorted guitar"
        descriptors.append("polluted skies")
    elif aqi > 100:
        tone = "hazy and somber"
        descriptors.append("urban fog")
    elif aqi <= 50:
        tone = "peaceful and clear"
        descriptors.append("fresh air")

    # 🧠 Compose final natural language prompt
    parts = [mood, tone] + descriptors
    filtered = list(filter(None, parts))
    sentence = ", ".join(filtered)
    prompt = f"A {sentence} {instrument} melody reflecting current environmental conditions."

    return prompt
