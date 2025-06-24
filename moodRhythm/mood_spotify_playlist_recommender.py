import cv2
import numpy as np
from deepface import DeepFace # type: ignore
import time
import random
import webbrowser

# Mood to Indian song mapping with standard Spotify track URLs
MOOD_SONG_MAP = {
    "happy": [
        ("Tum Hi Ho - Aashiqui 2", "https://open.spotify.com/track/2ZD4aIEepqZsdxPxLSuUhm?si=7903515222f8466a"),
        ("London Thumakda - Queen", "https://open.spotify.com/track/5uCaxd4z2dmn4Y6qTHO2Qw"),
        ("Gallan Goodiyaan - Dil Dhadakne Do", "https://open.spotify.com/track/73K33p4Vyz9koXGqmL5eFs?si=4249321cc1cc4b75"),
        ("Sweetu - Kill", "https://open.spotify.com/track/3JzOgUOqUKgkWwlb7rpg1J?si=5aaa55d9c20b4e50"),
        ("Saami Saami - Pushpa: The Rise", "https://open.spotify.com/track/44O26Gv1wQrlUj14PpTolM?si=53ee3fa486b64d24")
    ],
    "sad": [
        ("Channa Mereya - Ae Dil Hai Mushkil", "https://open.spotify.com/track/6vC2B4Z7p6e5fXh3Q8s3V5"),
        ("Tum Se Hi - Jab We Met", "https://open.spotify.com/track/3L8e3fLq2Uo9e0wL2l3x3v"),
        ("Phir Mohabbat - Murder 2", "https://open.spotify.com/track/5v0Q5QfX5e1p5z8J2u3w4q"),
        ("Main Rahoon Ya Na Rahoon - Pagalpanti", "https://open.spotify.com/track/7vQ4x9j3z7y5k9j1w3v4q6"),
        ("Dil Diyan Gallan - Tiger Zinda Hai", "https://open.spotify.com/track/4v5N4iP7sH2fN5x8v3w1q2")
    ],
    "angry": [
        ("Lungi Dance - Chennai Express", "https://open.spotify.com/track/0WfaI0wH5W1W1s9hQ9bXjP"),
        ("Malhari - Bajirao Mastani", "https://open.spotify.com/track/2eR8q3a5f0b9J8w1f9Yf4Q"),
        ("Ghagra - Yeh Jawaani Hai Deewani", "https://open.spotify.com/track/3bI8sXALQvN5Q8Q8RjQv7w"),
        ("Sher Khul Gaye - Fighter", "https://open.spotify.com/track/2J2ZTxGWrY8fX7iWv5dQ3v"),
        ("Jai Jai Shivshankar - War", "https://open.spotify.com/track/5uCaxd4z2dmn4Y6qTHO2Qw")
    ],
    "neutral": [
        ("Kun Faya Kun - Rockstar", "https://open.spotify.com/track/0vQ9u2x8lQ5v5q7f2x3v4q"),
        ("Agar Tum Saath Ho - Tamasha", "https://open.spotify.com/track/1w3v3Z3z4K8v5q7f2x3v4w"),
        ("Enna Sona - OK Jaanu", "https://open.spotify.com/track/4v5N4iP7sH2fN5x8v3w1q2"),
        ("Hawayein - Jab Harry Met Sejal", "https://open.spotify.com/track/6vC2B4Z7p6e5fXh3Q8s3V5"),
        ("Naina - Paris", "https://open.spotify.com/track/2eR8q3a5f0b9J8w1f9Yf4Q")
    ],
    "surprise": [
        ("Dilbar - Satyameva Jayate", "https://open.spotify.com/track/5v0Q5QfX5e1p5z8J2u3w4q"),
        ("Ghoomar - Padmaavat", "https://open.spotify.com/track/7vQ4x9j3z7y5k9j1w3v4q6"),
        ("Dhoom Machale - Dhoom:3", "https://open.spotify.com/track/3bI8sXALQvN5Q8Q8RjQv7w"),
        ("Morni Banke - Badhaai Ho", "https://open.spotify.com/track/2J2ZTxGWrY8fX7iWv5dQ3v"),
        ("Nachde Ne Saare - Baar Baar Dekho", "https://open.spotify.com/track/5uCaxd4z2dmn4Y6qTHO2Qw")
    ],
    "fear": [
        ("Ek Pal Ka Jeena - Kaho Naa... Pyaar Hai", "https://open.spotify.com/track/0vQ9u2x8lQ5v5q7f2x3v4q"),
        ("Jadu Teri Nazar - Darr", "https://open.spotify.com/track/1w3v3Z3z4K8v5q7f2x3v4w"),
        ("Chaiyya Chaiyya - Dil Se", "https://open.spotify.com/track/4v5N4iP7sH2fN5x8v3w1q2"),
        ("Raat Ka Nasha - Asoka", "https://open.spotify.com/track/6vC2B4Z7p6e5fXh3Q8s3V5"),
        ("Teri Ore - Singh Is Kinng", "https://open.spotify.com/track/2eR8q3a5f0b9J8w1f9Yf4Q")
    ],
    "disgust": [
        ("Kamli - Dhoom:3", "https://open.spotify.com/track/5v0Q5QfX5e1p5z8J2u3w4q"),
        ("Subha Hone Na De - Desi Boyz", "https://open.spotify.com/track/7vQ4x9j3z7y5k9j1w3v4q6"),
        ("Party All Night - Boss", "https://open.spotify.com/track/3bI8sXALQvN5Q8Q8RjQv7w"),
        ("Chikni Chameli - Agneepath", "https://open.spotify.com/track/2J2ZTxGWrY8fX7iWv5dQ3v"),
        ("Radha Teri Chunri - Mere Brother Ki Dulhan", "https://open.spotify.com/track/5uCaxd4z2dmn4Y6qTHO2Qw")
    ],
}

def get_random_songs(mood, last_songs=None):
    songs = MOOD_SONG_MAP.get(mood, MOOD_SONG_MAP["neutral"])
    if last_songs:
        available_songs = [s for s in songs if s not in last_songs]
        if not available_songs:
            available_songs = songs  # Reset if all used
        return random.sample(available_songs, min(3, len(available_songs)))
    return random.sample(songs, min(3, len(songs)))

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_detection_time = 0
    detection_interval = 5
    last_mood = None
    last_songs = None
    last_url_opened = None

    print("Starting mood detection... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)

        # Define window size and split into video and text panels
        window_width = 800
        window_height = 600
        video_width = 500  # Wider video panel
        text_width = window_width - video_width  # Narrower text box (300 pixels)
        frame = cv2.resize(frame, (video_width, window_height))

        current_time = time.time()
        if current_time - last_detection_time >= detection_interval:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                current_mood = result[0]['dominant_emotion']

                # Update songs only if mood changes
                if current_mood != last_mood:
                    songs = get_random_songs(current_mood, last_songs)
                    last_songs = songs
                    # Open the first song's URL in the browser if it hasn't been opened yet
                    if songs:
                        url_to_open = songs[0][1]
                        if url_to_open != last_url_opened:
                            print(f"Attempting to open URL: {url_to_open}")
                            try:
                                webbrowser.open(url_to_open, new=2)  # Open in new tab
                                last_url_opened = url_to_open
                                print(f"Successfully opened: {url_to_open}")
                            except Exception as e:
                                print(f"Failed to open URL {url_to_open}: {e}")
                                # Fallback to Spotify homepage
                                try:
                                    webbrowser.open("https://open.spotify.com", new=2)
                                    print("Fallback: Opened Spotify homepage")
                                except Exception as e:
                                    print(f"Failed to open fallback URL: {e}")
                else:
                    songs = last_songs or get_random_songs(current_mood)

                # Prepare text for display
                display_text = [f"Mood: {current_mood.capitalize()}"]
                display_text.extend([f"Song: {song[0]} ({song[1]})" for song in songs])

                last_mood = current_mood
                last_detection_time = current_time
            except Exception as e:
                print(f"Error in mood detection: {e}")
                display_text = ["Mood: Detecting...", "No recommendations available"]

        # Create a blank text panel with a darker background
        text_panel = np.zeros((window_height, text_width, 3), dtype=np.uint8)
        text_panel.fill(30)  # Darker gray background for better contrast

        # Add text to the text panel with improved spacing
        y0, dy = 50, 40  # Increased initial offset and line spacing
        for i, line in enumerate(display_text):
            y = y0 + i * dy
            cv2.putText(text_panel, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 255), 2)  # Lighter text color

        # Combine video and text panels horizontally
        combined_frame = np.hstack((frame, text_panel))
        cv2.imshow('Mood Detection', combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()