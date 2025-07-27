import sys
import os
from datetime import datetime

# Ensure dynamic import works regardless of where script is run from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ecoorchestra.data.fetcher import fetch_environment_data
from ecoorchestra.music.env_to_prompt import map_env_to_prompt
from ecoorchestra.music.musicgen_infer import generate_music_from_prompt

OUTPUT_DIR = "output/generated"

def get_user_location():
    """
    Prompt user for city, state, and country.
    """
    print("📍 Enter Location for AI Music Generation:")
    city = input("City: ").strip()
    state = input("State: ").strip()
    country = input("Country: ").strip()

    if not city or not state or not country:
        print("❌ All fields are required. Please try again.\n")
        return get_user_location()

    return city, state, country

def save_filename():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"eco_music_{timestamp}.wav")

def run_pipeline():
    print("\n🚀 Running EcoOrchestra AI Music Pipeline...\n")

    # Step 1: Prompt for location
    city, state, country = get_user_location()

    # Step 2: Fetch environmental data
    try:
        env_data = fetch_environment_data(city=city, state=state, country=country)
        print(f"\n🌍 Environmental Data:\n{env_data}")
    except Exception as e:
        print(f"❌ Failed to fetch environmental data: {e}")
        return

    # Step 3: Generate prompt from data
    prompt = map_env_to_prompt(**env_data)
    print(f"\n🎯 MusicGen Prompt:\n{prompt}")

    # Step 4: Generate audio
    audio_path = save_filename()
    try:
        generate_music_from_prompt(prompt, audio_path)
        print(f"\n✅ Music saved to: {audio_path}")
    except Exception as e:
        print(f"❌ Failed to generate music: {e}")

if __name__ == "__main__":
    run_pipeline()
