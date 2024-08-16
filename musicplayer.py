from tkinter import *
from tkinter import filedialog
import pygame
import os

# function to select audio
def select_audio(audio_file):

    pygame.mixer.music.stop()
    audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", ".mp3 .ogg .wav")])

    
    if audio_file:
        pygame.mixer.music.load(audio_file)

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
    root.geometry("300x125")
    root.resizable(False, False)
    # define audio_file
    audio_file = ""

    # play button
    play = Button(root, text="play", width = 5, font=("Courier New", 15), command=lambda: pygame.mixer.music.play())

    play.place(x=50,y=35)

    # stop button
    stop = Button(root, text="stop", width = 5, font=("Courier New", 15), command=lambda: pygame.mixer.music.stop())

    stop.place(x=175, y=35)

    # button to browse files
    browseFiles = Button(root, text="Browse Files...", width = 15, font=("Courier New", 8), command=lambda: select_audio(audio_file))

    browseFiles.place(x=0, y=0)

    # scale for volume
    volume = 100
    volumeScale = Scale(root, variable=volume,
                        from_ = 100, to = 0,
                        orient = VERTICAL,
                        command=adjust_vol)
    
    volumeScale.place(x=257, y=0)
    
    volumeScale.set(100)

    # main loop for the window
    root.mainloop()

main()