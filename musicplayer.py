from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pygame
import os

from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE




# function to select audio
def select_audio(audio_file):

    pygame.mixer.music.stop()
    audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", ".mp3 .ogg .wav")])
    
    global audioMetadata

    if audio_file:
        try:
            pygame.mixer.music.load(audio_file)

            if audio_file.endswith(".mp3"):
                audioMetadata = MP3(audio_file)
            elif audio_file.endswith(".wav"):
                audioMetadata = WAVE(audio_file)
            elif audio_file.endswith(".ogg"):
                audioMetadata = OggVorbis(audio_file)

            hours = int(audioMetadata.info.length/3600)
            minutes = int(audioMetadata.info.length/60)
            seconds = int(audioMetadata.info.length-(60*minutes))
            print(audioMetadata.info.length, hours, minutes, seconds )
        except pygame.error:
            messagebox.showerror(title="Error Reading File", message="This file was not able to be read. Try another.")

    return audioMetadata

        
# function to print artist and song title
def getSongTitle(audio_file, audioMetadata, songTitle, duration):
    songTitle = ""

def getDuration():

    global audioMetadata
    global duration

    hours = int(audioMetadata.info.length/3600)
    minutes = int(audioMetadata.info.length/60)
    seconds = int(audioMetadata.info.length-(60*minutes))

    hoursString = ""
    minutesString = ""
    secondsString = ""

    if hours < 10:
        hoursString = "0" + str(hours)
    else:
        hoursString = str(hours)
    
    if minutes < 10:
        minutesString = "0" + str(minutes)
    else:
        minutesString = str(hours)

    if seconds < 10:
        secondsString = "0" + str(seconds)
    else:
        secondsString = str(seconds)

    duration = (hoursString + ":" + minutesString + ":" + secondsString)

def setDuration(durationLabel):
    global duration
    
    durationLabel.config(text = duration)

def adjust_vol(volume):
    volumePy = float(volume)/100

    pygame.mixer.music.set_volume(volumePy)

# main function
def main():
    pygame.init() # initalize pygame

    # initalize the mixer for pygame
    pygame.mixer.init()

    # create window
    root = Tk()

    # attributes of the window
    root.title("Music Player")
    root.geometry("320x125")
    root.resizable(False, False)

    # define audio_file
    audio_file = ""


    # play button
    play = Button(root, text="play", 
                  width = 5, 
                  font=("Courier New", 15), 
                  command=lambda: pygame.mixer.music.play())

    play.place(x=50,y=35)

    # stop button
    stop = Button(root, text="stop", 
                  width = 5, 
                  font=("Courier New", 15), 
                  command=lambda: pygame.mixer.music.stop())

    stop.place(x=175, y=35)

    # button to browse files
    browseFiles = Button(root, text="Browse Files...", 
                         width = 15, font=("Courier New", 8), 
                         command=lambda: [select_audio(audio_file), getDuration(), setDuration(durationLabel)])

    browseFiles.place(x=0, y=0)

    # scale for volume
    volume = 100
    volumeScale = Scale(root, variable=volume,
                        from_ = 100, to = 0,
                        orient = VERTICAL,
                        command=adjust_vol)
    
    volumeScale.place(x=257, y=0)
    
    volumeScale.set(100)

    volumeLabel = Label(root, text="Volume",
                        font=("Courier New", 8))
    
    volumeLabel.place(x=265, y=100)

    durationLabel = Label(root, text="No Song Selected",
                     font=("Courier New", 8))
    
    durationLabel.place(x=100, y=100)
    # main loop for the window
    root.mainloop()

main()