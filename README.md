# Sarah - Voice-Controlled AI Chatbot

**Sarah** is a voice-controlled AI chatbot that can predict house prices based on user input, tell the time and date in a specific city, provide weather updates, tell jokes, and respond to greetings. It uses a trained machine learning pipeline to make real estate predictions, and responds to spoken inputs using speech recognition and text-to-speech.

---

## 💡 Features

- 🎙️ Voice-based interface for hands-free interaction.
- 🏡 Predict house prices based on location, income, and other features.
- 🌍 Tell local time and date for cities around the world.
- ⛅ Get real-time weather updates for a city.
- 😂 Tell random jokes.other features
- 👋 Respond to greetings, thanks, and goodbyes.
- ✈️ Predict flight delays based on factors like airline, scheduled departure time, and other features.
---

## 🧠 Technologies Used

- `speech_recognition`: For capturing user voice input.
- `pyttsx3`: For converting text to speech.
- `joblib`: For loading the trained machine learning model pipeline.
- `word2number`: For converting spoken numbers to numeric values.
- `pandas`: For data handling and feature formatting.
- `asyncio`: For async operations (e.g., weather).
- `pyjokes`: For telling jokes.
- Custom modules in `sarah_module`: Handles speech-to-text, text-to-speech, weather, and time.

---

## 🛠️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/linh672/Sarah_v2.git
   cd Sarah_v2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Git LFS** (if not already):
   ```bash
   git lfs install
   ```

4. **Pull large model file:**
   ```bash
   git lfs pull
   ```

5. **Run the chatbot:**
   ```bash
   python Sarah_v2_core.py
   ```

---

## 🏗️ How It Works

- Wake Sarah by saying **"wake up Sarah"**.
- Ask **"how to predict house price"** to get guidance.
- Start prediction with **"predict house price"** or **"predict flight delay"**.
- Sarah will ask for input feature-by-feature. You respond with values like:

  ```
  median income is thirty thousand 
  ocean proximity is near ocean
  ```

- Sarah will process and make a prediction using a trained model pipeline.
- You can also say things like:

  - **"What's the time in New York?"**
  - **"Tell me the weather in Tokyo"**
  - **"Tell me a joke"**
  - **"Goodbye"**

---

## 📁 Project Structure

```
Sarah_v2/
├── Sarah_v2_core.py             # Voice prediction logic
├── sarah_module/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── basic_module.py
│   └── ...
├── house_price_predictor/
│   ├── _house_price_model.pkl   # Trained model (Git LFS)
├── flight_delay_predictor                               
│   ├── _flight_delay_model.pkl
│   ├── _label_encoder.pkl
├── sarah_module/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── basic_module.py
│   └── ...
└── README.md
```
