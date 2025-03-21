import os
import random
import subprocess
from sr_tts import say

# Define the music folder path
MUSIC_FOLDER = "C:/Users/Lenovo/Music"
WMP_PATH = "C:/Program Files/Windows Media Player/wmplayer.exe"  # Full path

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
        self.current_process = None  # Stores the process of the playing song

    def play_music(self):
        """
        Plays the current song based on the current index.
        """
        current_song = self.music_files[self.current_index]
        print(f"\nPlaying: {os.path.basename(current_song)}", flush=True)
        say(f"Playing {os.path.basename(current_song)}")

        # Stop the previous song if it's playing
        self.stop_music()

        # Open music with Windows Media Player (full path)
        self.current_process = subprocess.Popen([WMP_PATH, current_song])

    def stop_music(self):
        """
        Stops the currently playing music.
        """
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None

    def pause_music(self):
        """
        Pauses the current music by stopping the process.
        """
        if self.current_process:
            self.stop_music()
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
