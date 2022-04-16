from operator import truediv
from textwrap import indent
from gtts import gTTS
from pygame import mixer
import pygame
from playsound import playsound
from humanfriendly import format_timespan
from tkinter import filedialog as fd
import os
import csv
import random
import threading
import time
import random
from art import text2art
from timer import Timer

running = True

mixer.init()
pygame.init()

class Exicise:
    def __init__(self, type, length):
        self.type = type
        self.length = length
    def str(self):
        return(format_timespan(int(self.length)) + "of" + self.type)
        
class Workout:
    def __init__(self, path):
        self.path = path
        self.excises = []
    
    def load(self):
        filepath = self.path
        if(os.path.exists(filepath)):
            f = open(filepath, "r")
            reader = csv.DictReader(f)
            for row in reader:
                self.excises.append(Exicise(row["exicise"], row["length"]))
            f.close()
        else:
            print("Workout.csv not found!")

    def save(self):
        filepath = self.path

        f = open(filepath, "w")
        fieldnames = ['exicise', 'length']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for e in self.excises:
            writer.writerow({'exicise': e.type, 'length': e.length})
        f.close()
def tts(texti): 
    speech = gTTS(text=texti)
    speech.save('tts.mp3')
    playsound('tts.mp3')
    os.remove('tts.mp3')

def songThreadFunction():
    playlist = os.listdir("songs")
    random.shuffle(playlist)
    currPlaylist = []
    for i in playlist:
        currPlaylist.append(i)
    pygame.mixer.music.load("songs/" + (currPlaylist[0]))
    currPlaylist.pop(0)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if len(currPlaylist) > 0:
                    pygame.mixer.music.load("songs/" + (currPlaylist[0]))
                    currPlaylist.pop(0)
                    pygame.mixer.music.play()
                else:
                    for i in playlist:
                        currPlaylist.append(i)
                    
                    pygame.mixer.music.load("songs/" + (currPlaylist[0]))
                    currPlaylist.pop(0)
                    pygame.mixer.music.play()


while running:
    print("======================================================")
    art=text2art("Workout")
    print(art)
    print("Options:")
    print("1 - Start New Workout")
    print("2 - Create Workout")
    print("3 - Quit")
    print("======================================================")
    selection = input("Input > ")
    if (selection == "1"):
        t = Timer()
        howMany = int(input("How Many Cycles of Workout? > "))
        workout = Workout("workout.csv")
        workout.load()
        x = threading.Thread(target=songThreadFunction)
        x.start()
        tts("starting in 10 seconds")
        time.sleep(5)
        playsound('timer.mp3')
        t.start()
        tts("Begin")
        for i in range(howMany):
            index = -1
            for e in workout.excises:
                index += 1
                if (index != 0):
                    tts("10 second rest, next exercise: " + e.type)
                    time.sleep(5)
                    playsound('timer.mp3')
                text = e.str()
                tts(text)
                time.sleep(int(e.length) - 5)
                playsound('timer.mp3')
            if(howMany > 1):
                if (i == howMany):
                    tts("Complete")
                    t.stop()
                else:
                    if (i == 0):
                        tts("1 Cycle Completed")
                        tts("10 second rest")
                        time.sleep(10)
                    else: 
                        tts(str(i + 1) + " Cycles Completed")
                        tts("10 second rest")
                        time.sleep(10)
            else:
                tts("complete")
                t.stop()
        running = False
    elif (selection == "2"):
        workout = Workout(workout.csv)
    elif (selection == "3"):
        running = False

    else:
        print("Invalid Selection")
