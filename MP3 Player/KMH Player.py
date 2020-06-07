#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk as tkk
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from pygame import mixer


window = tk.Tk()
window.title("MKH Player") 
window.geometry('800x450')
window.resizable(0, 0)

canvas=Canvas(window,width=800,height=450)
bgImg=PhotoImage(file = r"bgImg.png")
canvas.create_image(0,0,anchor=NW,image=bgImg)
canvas.pack()

menubar = Menu(window, bg='black')
window.config(menu=menubar)


subMenu = Menu(menubar, tearoff=0)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)
    
def trackinfo():
    l = playlistbox
    posList = l.curselection()

    if not posList:
        return

    for pos in posList:

        if pos == 0:
            continue
    audio = ID3(playlist[pos])
    artist = ("Artist: %s" % audio['TPE1'].text[0])
    track =( "Track: %s" % audio["TIT2"].text[0])
    tracklabel['text'] = artist + "\n" + track



    
def add_to_playlist(filename):
    filename = os.path.basename(filename)
    playlistbox.insert(0, filename)
    playlist.insert(0, filename_path)
    
def up():
    l = playlistbox
    posList = l.curselection()

    if not posList:
        return

    for pos in posList:
        if pos == 0:
            return
        buff = playlist[pos]
        playlist[pos] = playlist[pos-1]
        playlist[pos-1] = buff
        text = l.get(pos)
        l.delete(pos)
        l.insert(pos-1, text)
        playlistbox.selection_set(pos-1)
        
def down():
    l = playlistbox
    posList = l.curselection()

    if not posList:
        return

    for pos in posList:
        if pos == l.size()-1:
            return
        buff = playlist[pos]
        playlist[pos] = playlist[pos+1]
        playlist[pos+1] = buff
        text = l.get(pos)
        l.delete(pos)
        l.insert(pos+1, text)
        playlistbox.selection_set(pos+1)
        
def playNdInfo():
    trackinfo()
    play_music()

menubar.add_cascade(label="File", menu=subMenu, foreground= 'white')
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=window.destroy)

mixer.init()


playlistbox = Listbox(window, bg='black', fg='#ffffff')
playlistbox.place(width=450, height = 360)
playlistbox.place(x=10,y=80)

addBtn = tk.Button(window, text="+ Add", command=browse_file,background='black', foreground='white')
addBtn.place(width=110,height = 35)
addBtn.place(x=10,y=10)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = tk.Button(window, text="- Del", command=del_song,background='black', foreground='white')
delBtn.place(height=35, width=110)
delBtn.place(x=120,y=10)


lengthlabel = ttk.Label(window, text='Total Length : --:--',background='black', foreground='white')
lengthlabel.place(x=240,y=10)

currenttimelabel = ttk.Label(window, text='Current Time : --:--',background='black', foreground='white', relief=GROOVE)
currenttimelabel.place(x=240,y = 27)

tracklabel = ttk.Label(window, text='                            Track Info',background='black', foreground='white', relief=GROOVE)
tracklabel.place(width=330, height=55)
tracklabel.place(x=465,y = 385)



def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():

    global paused
    
    if paused:
        mixer.music.unpause()
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            show_details(play_it)
            
        except:
            tkinter.messagebox.showerror('File not found')


def stop_music():
    mixer.music.stop()



paused = FALSE

def sortArtist():
    l = playlistbox
    flag = 1
    i = 0
    while(flag is not 0):
        flag = 0
        for j in range(1, l.size()-i):
            audio = ID3(playlist[j-1])
            song1 = (audio['TPE1'].text[0])
            audio = ID3(playlist[j])
            song2 = (audio['TPE1'].text[0])
                
            if(song1>song2):
                buff = playlist[j-1]
                playlist[j-1] = playlist[j]
                playlist[j] = buff
                text = l.get(j-1)
                l.delete(j-1)
                l.insert(j, text)
                flag = 1
        i = i+1
        
                
def sortTitle():
    l = playlistbox
    flag = 1
    i = 0
    while(flag is not 0):
        flag = 0
        for j in range(1, l.size()-i):
            #audio = ID3(playlist[j-1])
            song1 = playlist[j-1]
            #audio = ID3(playlist[j])
            song2 = playlist[j]
                
            if(song1>song2):
                buff = playlist[j-1]
                playlist[j-1] = playlist[j]
                playlist[j] = buff
                text = l.get(j-1)
                l.delete(j-1)
                l.insert(j, text)
                flag = 1
        i = i+1

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()



def rewind_music():
    play_music()



def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(1.0)
        volumeBtn.configure(image=volumePhoto)
        scale.set(100)
        muted = FALSE
    else:  
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


rewindPhoto = PhotoImage(file= r"wrewind.png")
rewindBtn = tk.Button(window, image=rewindPhoto, command=rewind_music,bg='black')
rewindBtn.place(x=515,y=45)

playPhoto = PhotoImage(file= r"wplay.png")
playBtn = tk.Button(window, image=playPhoto, command=playNdInfo,bg='black')
playBtn.place(x=565,y=45)

stopPhoto = PhotoImage(file= r"wstop.png")
stopBtn = tk.Button(window, image=stopPhoto,command=stop_music,bg='black')
stopBtn.place(x=625,y=45)

pausePhoto = PhotoImage(file= r"wpause.png")
pauseBtn = tk.Button(window, image=pausePhoto, command=pause_music,bg='black')
pauseBtn.place(x=685,y=45)

mutePhoto = PhotoImage(file= r"wmute.png")
volumePhoto = PhotoImage(file= r"wvolume.png")
volumeBtn = tk.Button( image=volumePhoto, command=mute_music,bg='black')
volumeBtn.place(x=745,y=45)

btnArtist = tk.Button(window, text = "Sort by artist", bg='black',command = sortArtist, foreground='white')
btnArtist.place(x=10,y=50)
btnArtist.place(height=25, width=220)

btnTitle = tk.Button(window, text = "Sort by title", bg='black', command = sortTitle, foreground='white')
btnTitle.place(x=240,y=50)
btnTitle.place(height=25, width=220)


upPhoto = PhotoImage(file= r"up.png")
upBtn = tk.Button(window, image=upPhoto, command=up,bg='black')
upBtn.place(x=465,y=210)

downPhoto = PhotoImage(file= r"down.png")
downBtn = tk.Button(window, image=downPhoto, command=down,bg='black')
downBtn.place(x=465,y=250)

scale = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL,command=set_vol)
scale.set(100)
mixer.music.set_volume(1.0)
scale.place(x=590,y=15)


def on_closing():
    stop_music()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()