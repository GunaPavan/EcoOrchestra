EcoOrchestra 🌿🎶
Generative AI music from real-time environmental data. Giving nature a voice.
EcoOrchestra transforms live environmental data (temperature, humidity, AQI, wind) into emotionally resonant music using state-of-the-art AI models. It aims to raise environmental awareness by letting people hear the condition of our planet.
✨ Features

🌍 Fetches real-time environmental data (weather + AQI).
🎵 Maps data into AI-generated music prompts.
🤖 Uses MusicGen (Meta) for creative audio synthesis.
💻 Streamlit frontend for interactive use.
📂 Saves generated tracks locally for reuse.

📦 Installation
Clone the repository:
git clone https://github.com/GunaPavan/EcoOrchestra.git
cd EcoOrchestra

Create and activate a virtual environment with uv:
uv venv .venv
.venv\Scripts\activate   # On Windows
# or source .venv/bin/activate  # On macOS/Linux

Install dependencies:
uv sync

⚙️ Configuration
Create a .env file in the project root with your API keys:
OPENWEATHERMAP_API_KEY=your_openweathermap_key
AIRVISUAL_API_KEY=your_airvisual_key

🚀 Usage
Streamlit Frontend
Run the interactive app:
streamlit run frontend/app.py

Then open http://localhost:8501.
Generated audio files are saved in the output/generated/ directory.
📂 Project Structure
eco-orchestra/
├── frontend/
│   ├── app.py
│   ├── output/
│   └── src/
│       └── ecoorchestra/
│           ├── __pycache__/
│           ├── data/
│           │   └── __pycache__/
│           ├── __init__.py
│           └── fetcher.py
├── music/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── env_to_prompt.py
│   ├── musicgen_infer.py
│   └── pipeline/
│       ├── main_pipeline.py
│       └── __init__.py
├── tests/
│   └── test_fetcher.py
├── .env
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock

🛡️ License
This project is released under the MIT License.