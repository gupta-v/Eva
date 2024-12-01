import os
import random
import subprocess
from sr_tts import say

# Define the music folder path
MUSIC_FOLDER = "C:/Users/Lenovo/Music"

class MusicPlayer:
    def __init__(self):
        """
        Initializes the music player with the predefined folder containing music files.
        """
        self.music_folder = MUSIC_FOLDER
        self.music_files = [
            os.path.join(self.music_folder, f)
            for f in os.listdir(self.music_folder)
            if f.endswith((".mp3", ".wav"))
        ]
        if not self.music_files:
            print("No music files found in the folder!", flush=True)
            say("No music files found in the folder!")
            raise FileNotFoundError("No music files found in the specified folder.")
        self.current_index = 0  # Tracks the current song index

    def play_music(self):
        """
        Plays the current song based on the current index.
        """
        current_song = self.music_files[self.current_index]
        print(f"\nPlaying: {os.path.basename(current_song)}", flush=True)
        say(f"Playing {os.path.basename(current_song)}")
        subprocess.call(["start", current_song], shell=True)

    def pause_music(self):
            """
            Pauses the current music by killing the process.
            """
            if self.current_process:
                print("\nPausing music...", flush=True)
                say("Pausing music")
                self.current_process.kill()
                self.current_process = None
            else:
                print("\nNo music is currently playing to pause!", flush=True)
                say("No music is currently playing to pause!")

    def next_song(self):
        """
        Moves to the next song and plays it.
        """
        self.current_index = (self.current_index + 1) % len(self.music_files)
        self.play_music()

    def previous_song(self):
        """
        Moves to the previous song and plays it.
        """
        self.current_index = (self.current_index - 1) % len(self.music_files)
        self.play_music()

    def shuffle_and_play(self):
        """
        Shuffles the playlist and plays the first song.
        """
        random.shuffle(self.music_files)
        self.current_index = 0
        self.play_music()


# Instantiate the player for direct use in the main app
player = MusicPlayer()