import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace  # type: ignore
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import random
import webbrowser
import csv
from datetime import datetime

MOOD_TO_KEYWORD = {
    "happy": "upbeat", "sad": "melancholy", "angry": "intense",
    "surprise": "party", "fear": "calm", "neutral": "chill", "disgust": "dark"
}

MOOD_EMOJIS = {
    "happy": "😄", "sad": "😢", "angry": "😠",
    "surprise": "😮", "fear": "😨", "neutral": "😐", "disgust": "🤢"
}

class MoodCamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Music Recommender 🎵")

        self.cap = cv2.VideoCapture(0)
        self.video_label = tk.Label(root)
        self.video_label.grid(row=0, column=0, padx=10, pady=10)

        self.info_frame = ttk.Frame(root)
        self.info_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        ttk.Label(self.info_frame, text="Detected Mood:", font=("Helvetica", 12)).pack(anchor='w')
        self.mood_var = tk.StringVar()
        ttk.Label(self.info_frame, textvariable=self.mood_var, font=("Helvetica", 16, "bold")).pack(anchor='w', pady=5)

        ttk.Label(self.info_frame, text="Language:", font=("Helvetica", 12)).pack(anchor='w', pady=(15, 0))
        self.language_var = tk.StringVar(value="English")
        ttk.OptionMenu(self.info_frame, self.language_var, "English", "Hindi", "Tamil", "Punjabi").pack(anchor='w')

        ttk.Label(self.info_frame, text="Recommended Song:", font=("Helvetica", 12)).pack(anchor='w', pady=(20, 0))
        self.song_var = tk.StringVar()
        ttk.Label(self.info_frame, textvariable=self.song_var, wraplength=250, font=("Helvetica", 14)).pack(anchor='w', pady=5)

        self.link_var = tk.StringVar()
        self.link_label = ttk.Label(self.info_frame, textvariable=self.link_var, foreground="blue", cursor="hand2", wraplength=250)
        self.link_label.pack(anchor='w')
        self.link_label.bind("<Button-1>", self.open_link)

        ttk.Button(self.info_frame, text="🎶 Generate Playlist", command=self.show_playlist).pack(anchor='w', pady=(25, 0))

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="985d6a5249c443da92a2cc0aca418edb",
            client_secret="a512d4fab6ef40f0a0409383448d971f",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-read-playback-state"
        ))

        self.last_mood = None
        self.last_check = time.time()
        self.cooldown = 8

        self.update_camera()
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            display = frame.copy()
            now = time.time()

            if now - self.last_check > self.cooldown:
                mood = self.detect_mood(display)
                if mood and mood != self.last_mood:
                    self.last_mood = mood
                    self.update_recommendation(mood)
                self.last_check = now

            try:
                faces = DeepFace.extract_faces(display, enforce_detection=False)
                for face in faces:
                    box = face['facial_area']
                    x, y, w, h = box['x'], box['y'], box['w'], box['h']
                    cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    emoji = MOOD_EMOJIS.get(self.last_mood, "")
                    label = f"{emoji} {self.last_mood.capitalize() if self.last_mood else ''}"
                    cv2.putText(display, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            except:
                pass

            rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_camera)

    def detect_mood(self, frame):
        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            result = result[0] if isinstance(result, list) else result
            return result.get("dominant_emotion")
        except Exception as e:
            print("Detection error:", e)
            return None

    def update_recommendation(self, mood):
        print(f"New mood detected: {mood}")
        self.mood_var.set(mood.capitalize())
        language = self.language_var.get()
        keyword = MOOD_TO_KEYWORD.get(mood.lower(), "pop")
        query = f"{keyword} {language}"
        track = self.get_track(query)
        if track:
            song = f"{track['name']} by {track['artists'][0]['name']}"
            link = track['external_urls']['spotify']
            self.song_var.set(song)
            self.link_var.set(link)

            # Log mood + track
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [timestamp, mood, track['name'], track['artists'][0]['name'], link]
            try:
                with open("mood_history.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if f.tell() == 0:
                        writer.writerow(["Timestamp", "Mood", "Track", "Artist", "Link"])
                    writer.writerow(row)
            except Exception as e:
                print("CSV Logging error:", e)
        else:
            self.song_var.set("No song found.")
            self.link_var.set("")
    def get_track(self, keyword):
        try:
            results = self.sp.search(q=keyword, type='track', limit=20)
            tracks = results.get('tracks', {}).get('items', [])
            return random.choice(tracks) if tracks else None
        except Exception as e:
            print("Spotify error:", e)
            return None

    def open_link(self, event):
        link = self.link_var.get()
        if link:
            webbrowser.open_new(link)

    def show_playlist(self):
        popup = tk.Toplevel(self.root)
        popup.title("Your Mood Playlist 🎶")
        popup.geometry("460x400")
        ttk.Label(popup, text="📝 Songs from your session:").pack(pady=10)

        box = tk.Listbox(popup, width=65, height=20)
        box.pack(padx=10, pady=5)

        try:
            with open("mood_history.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    line = f"{row['Mood'].capitalize()}: {row['Track']} by {row['Artist']}"
                    box.insert(tk.END, line)
        except FileNotFoundError:
            box.insert(tk.END, "No mood history available.")

    def close(self):
        self.cap.release()

        # Read mood history
        summary = []
        mood_count = {}

        try:
            with open("mood_history.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    mood = row["Mood"]
                    mood_count[mood] = mood_count.get(mood, 0) + 1
                    summary.append(f"{row['Timestamp']} — {mood.capitalize()}: {row['Track']} by {row['Artist']}")
            top_mood = max(mood_count, key=mood_count.get) if mood_count else "N/A"
            total = len(summary)
        except FileNotFoundError:
            summary = ["No mood history recorded."]
            top_mood = "N/A"
            total = 0

        popup = tk.Toplevel(self.root)
        popup.title("Today's Mood Summary")
        popup.geometry("440x400")
        ttk.Label(popup, text=f"🎧 You had {total} musical moments today.").pack(pady=5)
        ttk.Label(popup, text=f"💡 Most frequent mood: {top_mood.capitalize()}").pack(pady=5)

        box = tk.Listbox(popup, width=65, height=15)
        box.pack(padx=10, pady=10)
        for entry in summary:
            box.insert(tk.END, entry)

        ttk.Label(popup, text="Thanks for vibing, Dhruv! 🌈").pack(pady=10)
        ttk.Button(popup, text="Exit", command=self.root.destroy).pack(pady=5)
if __name__ == "__main__":
    root = tk.Tk()
    app = MoodCamApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()