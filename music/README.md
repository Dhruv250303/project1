# 🎵 MoodCam+  
**An Emotion-Aware Music Recommender Powered by Facial Recognition and Spotify**

MoodCam+ is a smart, expressive desktop app that detects your mood using your webcam and recommends mood-matching music in your preferred language. It’s like a mirror that reflects your feelings back as music—emoji and all.

---

## 🌟 Features

- 🎭 Real-time emotion detection via facial recognition (DeepFace)
- 🌍 Language support: English, Hindi, Tamil, Punjabi
- 🎶 Spotify-powered track recommendations based on mood & language
- 📸 Emoji + mood overlay on your live camera feed
- 📓 Mood history logging to `mood_history.csv`
- 📋 Playlist viewer for all recommended songs in a session
- 🎬 End-of-session vibe summary popup

---

## 💻 Tech Stack

| Component     | Technology             |
|---------------|------------------------|
| Language      | Python 3.9+            |
| GUI           | Tkinter                |
| Webcam Feed   | OpenCV                 |
| Emotion AI    | DeepFace               |
| Music API     | Spotify API via Spotipy|
| Image Tools   | Pillow                 |
| Data Logging  | CSV                    |

---

## 📸 Emotion-to-Music Mapping

| Detected Mood | Keyword      | Example Query           |
|---------------|--------------|--------------------------|
| Happy         | upbeat       | `upbeat Hindi`          |
| Sad           | melancholy   | `melancholy Tamil`      |
| Angry         | intense      | `intense Punjabi`       |
| Neutral       | chill        | `chill English`         |
| Surprise      | party        | `party Hindi`           |
| Fear          | calm         | `calm Tamil`            |
| Disgust       | dark         | `dark English`          |

---

## 🗂 How to Run

1. **Install Requirements:**

   ```bash
   pip install opencv-python deepface spotipy pillow
Here you go, Dhruv! Here’s the full content of your README.md file, ready to save directly:

Filename: README.md
# 🎵 MoodCam+  
**An Emotion-Aware Music Recommender Powered by Facial Recognition and Spotify**

MoodCam+ is a smart, expressive desktop app that detects your mood using your webcam and recommends mood-matching music in your preferred language. It’s like a mirror that reflects your feelings back as music—emoji and all.

---

## 🌟 Features

- 🎭 Real-time emotion detection via facial recognition (DeepFace)
- 🌍 Language support: English, Hindi, Tamil, Punjabi
- 🎶 Spotify-powered track recommendations based on mood & language
- 📸 Emoji + mood overlay on your live camera feed
- 📓 Mood history logging to `mood_history.csv`
- 📋 Playlist viewer for all recommended songs in a session
- 🎬 End-of-session vibe summary popup

---

## 💻 Tech Stack

| Component     | Technology             |
|---------------|------------------------|
| Language      | Python 3.9+            |
| GUI           | Tkinter                |
| Webcam Feed   | OpenCV                 |
| Emotion AI    | DeepFace               |
| Music API     | Spotify API via Spotipy|
| Image Tools   | Pillow                 |
| Data Logging  | CSV                    |

---

## 📸 Emotion-to-Music Mapping

| Detected Mood | Keyword      | Example Query           |
|---------------|--------------|--------------------------|
| Happy         | upbeat       | `upbeat Hindi`          |
| Sad           | melancholy   | `melancholy Tamil`      |
| Angry         | intense      | `intense Punjabi`       |
| Neutral       | chill        | `chill English`         |
| Surprise      | party        | `party Hindi`           |
| Fear          | calm         | `calm Tamil`            |
| Disgust       | dark         | `dark English`          |

---

## 🗂 How to Run

1. **Install Requirements:**

   ```bash
   pip install opencv-python deepface spotipy pillow

2. **Add Spotify Credentials:**
- Go to: Spotify Developer Dashboard
- Create an app → Get Client ID and Secret
- Paste them into the script under:

SpotifyOAuth(
  client_id="YOUR_CLIENT_ID",
  client_secret="YOUR_CLIENT_SECRET",
  ...
)
3. **Run the App:**
python MoodCam.py


## 💡 Future Enhancements- 
📊 Mood trends charting (line plots, emotion wheels)
- 📤 Export mood-based playlists to Spotify
- 🌗 Dark mode UI themes
- 🗣️ Voice narration: mood-to-speech responses
- 📱 Mobile camera integration

## 🧠 Credits:
Made by Dhruv
In collaboration with Microsoft Copilot, OpenCV, DeepFace, Spotify, and Python’s Tkinter."Your face made great music today." 🎧
---