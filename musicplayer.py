# TKinter imports
from tkinter import * # All the basic nonsense
from tkinter import filedialog # For selecting files
from tkinter import messagebox # For showing a message

# Pygame Import
import pygame

# OS Import
import os

# Import mutagen for reading metadata of audio files
from mutagen.mp3 import MP3 # MP3 Metadata reading capability
from mutagen.oggvorbis import OggVorbis # OGG Metadata reading capability
from mutagen.wave import WAVE # WAV Metadata reading capability

# For running code in the background
import threading

# Import time for waiting
import time

# function to select audio
def select_audio(audio_file, audioFileNameLabel):

    # Stop music from playing if music is already playing
    pygame.mixer.music.stop()

    # Prompt user to select a file from the following choices             Audio Files
    audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", ".mp3 .ogg .wav")])
    print(audio_file)
    
    # Global Audiometadata... which is probably not good practice but I'm learning
    global audioMetadata
    
    # If the audio is selected
    if audio_file:
        # Try the following code
        try:
            # Load the file
            pygame.mixer.music.load(audio_file)

            # If statements for if the audio file has a certain extension
            if audio_file.endswith(".mp3"):
                audioMetadata = MP3(audio_file)
            elif audio_file.endswith(".wav"):
                audioMetadata = WAVE(audio_file)
            elif audio_file.endswith(".ogg"):
                audioMetadata = OggVorbis(audio_file)

            # time variables for seeing how long the song is
            hours = int(audioMetadata.info.length/3600)
            minutes = int(audioMetadata.info.length/60)
            seconds = int(audioMetadata.info.length-(60*minutes))

            # print out the length in seconds and roughly format it 
            print(audioMetadata.info.length, hours, minutes, seconds )
        except pygame.error: # if a pygame error is thrown 
            # run this
            messagebox.showerror(title="Error Reading File", message="This file was not able to be read. Try another.")

    # split the audio_file path by the number of slashes(/) 
    res = audio_file.split("/", audio_file.count('/'))

    # get the audio_filename from that
    audio_fileName = res[-1]
    print(audio_fileName)

    # update the file name label and place
    audioFileNameLabel.config(text=audio_fileName)
    audioFileNameLabel.place(x=0, y=125)

    # return the audioMetadata
    return audioMetadata

# function to place song position down
def showPosition(songPositionLabel):
    # Place song position label
    songPositionLabel.place(x=20, y=100)

# function to print artist and song title, obviously not done at ALL
def getSongTitlenArtist(audioMetadata, titleArtistLabel):

    # Try the following code
    try:
    # trying to figure out audio title metadata tags
        if "TIT2" in audioMetadata.tags:
            songTitle = audioMetadata.tags["TIT2"] # if its an mp3 assign the title to songTitle
            print(songTitle) # print it out
        elif "title" in audioMetadata.tags: # if it's not an mp3 and it's an ogg or wav
            songTitle = audioMetadata.tags["title"] # assign the ogg/wav title to songTitle
            print(songTitle) # print out songTitle
        else: 
            songTitle = "Unknown Song" # if it's none of those/there is no title, assign Unknown Song to songTitle
            print(songTitle) # print out Unknown Song
    except TypeError: # If a type error is thrown then assign unknown song to songTitle
        songTitle = "Unknown Song"
        print(songTitle)
        
    try:
    # I'm not typing all that again, you get it
        if "TPE1" in audioMetadata.tags:
            songArtist = audioMetadata.tags["TPE1"]
            print(songArtist)
        elif "artist" in audioMetadata.tags:
            songArtist = audioMetadata.tags["artist"]
            print(songArtist)
        else:
            songArtist = "Unknown Artist"
            print(songArtist)
    except TypeError:
        songArtist = "Unknown Artist"
        print(songArtist)
    
    # Combine song title and song artist to show the complete thing
    titleArtistLabel.config(text=f"{songTitle}\nby\n{songArtist}")
    titleArtistLabel.place(x=120, y=0)


# Function to get the duration of a song
def getDuration():

    # two global variables. Why didn't I try looking up if this was a good idea
    global audioMetadata
    global duration

    # Time local variables
    hours = int(audioMetadata.info.length/3600)
    minutes = int(audioMetadata.info.length/60)
    seconds = int(audioMetadata.info.length-(60*minutes))

    # Holy crap, a way better formatted way of doing this jesus christ
    duration = f"{hours:02}:{minutes:02}:{seconds:02}"

# setter for duration, that's it nothing more
def setDuration(durationLabel):
    global duration
    
    # config the duration label
    durationLabel.config(text = duration)

# Getter Setter Combination for updating the song position
def updatePosition(songPositionLabel):
    # while the channel for music is busy
    while pygame.mixer.music.get_busy():
        songPosition = pygame.mixer.music.get_pos() / 1000 # convert the time to seconds

        # Time local variables
        hours = int(songPosition / 3600)
        minutes = int((songPosition % 3600) / 60)
        seconds = int(songPosition % 60)

        # better formated song position, like I said, holy shit it took me way too long to find this out
        songPositionStr = f"{hours:02}:{minutes:02}:{seconds:02}"
        songPositionLabel.config(text=songPositionStr + " /") # config the label to change while the channel is busy
        time.sleep(1)  # update every second

# easy function for adjusting volume
def adjust_vol(volume):
    # adjust the volume on the slider to be pygame sufficent
    volumePy = float(volume)/100 

    # set the volume of the music 
    pygame.mixer.music.set_volume(volumePy)

# main function - where all the fuckery happens and where all the commenting needs to be
def main():
    pygame.init() # initalize pygame

    # initalize the mixer for pygame
    pygame.mixer.init()

    # create window
    root = Tk()

    # attributes of the window
    root.title("Music Player")
    root.geometry("320x145")
    root.resizable(False, False)
    
    # make icon photo
    iconPhoto = PhotoImage(file="26205.png")
    root.iconphoto(False, iconPhoto)
    
    # define audio_file
    audio_file = ""

    # play button
    play = Button(root, text="play", 
                  width = 5, # width of the button
                  font=("Courier New", 15), # font and font size                                            dont even ask me how
                  command=lambda: [pygame.mixer.music.play(), threading.Thread(target=updatePosition, args=(songPositionLabel,)).start()]) # let music play and execute a functions (TOOK WAY TOO GOD DAMN LONG TO FIND OUT)
                                                                                                        #   a comma works here
    # place play button
    play.place(x=50,y=50)

    # stop button
    stop = Button(root, text="stop", 
                  width = 5, # width of the button
                  font=("Courier New", 15), # font and font size
                  command=lambda: pygame.mixer.music.stop()) # just stop the music. So easy to do :) I love you line 143. Mwah, you're so beautiful and simple

    # place stop button
    stop.place(x=175, y=50)

    # button to browse files
    browseFiles = Button(root, text="Browse Files...", 
                         width = 15, font=("Courier New", 8), 
                         command=lambda: [select_audio(audio_file, audioFileNameLabel), getDuration(), setDuration(durationLabel), showPosition(songPositionLabel), getSongTitlenArtist(audioMetadata, titleArtistLabel)]) # Execute 4 functions. So fancy.(not)

    # Place small button to browse files
    browseFiles.place(x=0, y=0)

    # scale for volume
    volume = 100 # volume variable
    volumeScale = Scale(root, variable=volume, # assign the slider the volume variable
                        from_ = 100, to = 0, # have the slider go from 100 to 0
                        orient = VERTICAL, # orient it vertically
                        command=adjust_vol) # execute adjust_vol function when the slider is used
    
    # Place slider
    volumeScale.place(x=257, y=0)
    
    # set the slider to 100
    volumeScale.set(100)

    # label to say "Hey! This is the volume slider :)"
    volumeLabel = Label(root, text="Volume",
                        font=("Courier New", 8))
    
    # place the volume label
    volumeLabel.place(x=265, y=100)

    # Label to show the duration which starts out saying "no song selected"
    durationLabel = Label(root, text="No Song Selected",
                          font=("Courier New", 8))
    
    # Label to show the current position of the song. Formatted weird because :3 
    songPositionLabel = Label(root, text="00:00:00 /",
                              font=("Courier New", 8))

    # Place duration label, dont ask me why the duration label is placed after the songPosition label
    durationLabel.place(x=100, y=100)

    # label for song title and song artist
    titleArtistLabel = Label(root, text="PlaceHolder Ipsum\nor\nwhatever",
                             font=("Courier New", 7))

    # label for the audio file name
    audioFileNameLabel = Label(root, text="No Song Selected",
                               font=("Courier New", 7))

    # main loop for the window
    root.mainloop()

# run main function
main()