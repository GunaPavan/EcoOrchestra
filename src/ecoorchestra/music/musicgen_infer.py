# src/ecoorchestra/music/musicgen_infer.py

import torch
from transformers import pipeline

print("🧠 Loading MusicGen pipeline...")
pipe = pipeline("text-to-audio", model="facebook/musicgen-small", device=0 if torch.cuda.is_available() else -1)
print("✅ MusicGen loaded successfully.")

def generate_music_from_prompt(prompt: str, output_path: str, duration_sec: int = 15):
    print(f"🎼 Generating music from prompt: \"{prompt}\"")
    try:
        outputs = pipe(prompt, forward_params={"do_sample": True, "max_new_tokens": duration_sec * 50})
        audio = outputs["audio"]
        sampling_rate = outputs["sampling_rate"]

        # Save as .wav
        from scipy.io.wavfile import write as write_wav
        import numpy as np

        audio_np = (audio * 32767).astype(np.int16)
        write_wav(output_path, rate=sampling_rate, data=audio_np)

        print(f"✅ Music generated and saved to: {output_path}")
    except Exception as e:
        print(f"❌ Music generation failed: {e}")
