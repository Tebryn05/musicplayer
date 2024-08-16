from tkinter import *
import pygame
import os

def play(audio):
    audio.play()

def main():
    pygame.init()

    pygame.mixer.init()

    root = Tk()

    root.title("Music Player Test")
    root.geometry("300x125")
    root.resizable(False, False)

    testMusic = pygame.mixer.Sound("sdre48.mp3")

    play = Button(root, text="play", width = 5, font=("Courier New", 15), command=lambda: testMusic.play())

    play.place(x=120,y=10)

    stop = Button(root, text="stop", width = 5, font=("Courier New", 15), command=lambda: testMusic.stop())


    stop.place(x=120, y=62)
    root.mainloop()

main()