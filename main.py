from flask import Flask, render_template,jsonify
import flask
import csv
import os
import threading
import tkinter as tk
from moviepy.editor import *
from pygame import mixer
from pytube import *
import yt_dlp
import pandas as pd
import SpotifyAPI
import Recommender
import requests
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/register", methods=["POST"])
def submit():
    username = flask.request.form.get("username")
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    username = username.strip()
    email = email.strip()
    password = password.strip()

    
    with open("/"+username+"/user_data.csv", mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([username,email, password])
    f=open(username+".csv",mode="w",newline="")
    f.close()
    return render_template("player.html")
@app.route("/login", methods=["POST"])
def login():
    email = flask.request.form.get("email")
    password =flask.request.form.get("password")
    email = email.strip()
    password = password.strip()
    login_successful = False
    with open("user_data.csv", mode="r", newline="") as csv_file:
            csv_read = csv.reader(csv_file)
            for row in csv_read:
                print(row)
                if (email==row[1] and password==row[2]):  
                    
                    login_successful = True
                    break  

    if login_successful:
            return render_template("homepage.html")
    else:
            return render_template("loginpage.html")
class Node:
    def __init__(self, link=None):
        self.linker = link
        self.nextval = None
        self.preval = None

class LinkedList:
    def __init__(self):
        self.headval = None
        self.start = None
class MusicPlayer:
    def __init__(self):
        self.y, self.z = 0, 0
        self.var = 0
        self.le = 0
        self.repeat=False
        self.cwd = os.getcwd()
        self.l = LinkedList()
        self.music_thread = None

    def inputer(self):
        self.l = LinkedList()
        f = open(os.path.join(self.cwd, "playlist", "musicfiles.txt"), "r", encoding='utf-8')
        r = f.readlines()
        j=0
        for i in r:
            j += 1
            if j == 1:
                a = Node(i)
                self.l.headval = a
                self.l.start = a
                a.nextval = self.l.start
                a.preval = self.l.start
            else:
                a = Node(i)
                self.l.start.nextval = a
                a.preval = self.l.start
                a.nextval = self.l.headval
                self.l.headval.preval = a
                self.l.start = a
    def temp_inputer(self):
        self.l = LinkedList()
        f = open(os.path.join(self.cwd, "playlist", "queue.txt"), "r", encoding='utf-8')
        r = f.readlines()
        j=0
        for i in r:
            j += 1
            if j == 1:
                a = Node(i)
                self.l.headval = a
                self.l.start = a
                a.nextval = self.l.start
                a.preval = self.l.start
            else:
                a = Node(i)
                self.l.start.nextval = a
                a.preval = self.l.start
                a.nextval = self.l.headval
                self.l.headval.preval = a
                self.l.start = a

    def autoplay(self):
        while True:
            if self.var != 3:
                os.chdir(os.path.join(self.cwd, 'playlist'))
                mixer.music.load(self.l.start.linker[:-1])
                mixer.music.play()
                os.chdir(self.cwd)
            else:
                mixer.music.unpause()
                self.var = 0
            while mixer.music.get_busy():
                continue
            if self.var == 1:
                self.var = 0
                break
            if self.var == 2:
                break
            if self.repeat==False:
                self.l.start = self.l.start.nextval

    def next1(self):
        self.var = 1
        self.stop()
        self.music_thread.join()
        self.l.start = self.l.start.nextval
        self.music_thread = threading.Thread(target=self.autoplay)
        self.music_thread.start()
    def repeater(self):
        self.repeat=True
    def norep(self):
        self.repeat=False
    def prev(self):
        self.var = 1
        self.stop()
        self.music_thread.join()
        self.l.start = self.l.start.preval
        self.music_thread = threading.Thread(target=self.autoplay)
        self.music_thread.start()

    def play(self):
        self.l.start = self.l.headval
        print(self.l.start.linker)
        mixer.init()
        self.music_thread = threading.Thread(target=self.autoplay)
        self.music_thread.start()
    def playcurr(self,link):
        if(mixer.music.get_busy()):
            self.stop()
        a=self.l.headval
        print(a.linker+"Reach")
        while(True):
            if link in a.linker:
                self.l.headval=a
                print(self.l.headval.linker+"VANDHUTEN")
                break
            a=a.nextval
    def pause(self):
        self.var = 2
        mixer.music.pause()
        self.music_thread.join()

    def unpause(self):
        self.var = 3
        self.music_thread = threading.Thread(target=self.autoplay)
        self.music_thread.start()

    def stop(self):
        self.var = 1
        mixer.music.stop()
        mixer.music.unload()
        self.music_thread.join()
    def proc(self,userinput):
        a = Search(userinput)
        result = a.results
        return result
    def download_audio(self, link):
        ydl_opts = {
        'format': 'worstvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'extract_audio': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as video:
            info_dict = video.extract_info(link, download=True)
            video_title = info_dict['title']
            return video_title
    def name(self, link):
        y={}
        with yt_dlp.YoutubeDL(y) as video:
            info_dict = video.extract_info(link, download=False)
            video_title = info_dict['title']
            return video_title
    def search(self,result,s):
        query = ((str(result).split("="))[-1])[0:-1]
        os.chdir(os.path.join(self.cwd, 'static'))
        mixer.music.load("Bad Piggies Theme [EgAOqt8I5ac].mp3")
        mixer.music.play()
        os.chdir(self.cwd)
        vidname = self.download_audio('https://www.youtube.com/watch?v=' + query)
        vidname += " [" + query + "]"
        vidname = vidname.replace('|', '｜')
        vidname = vidname.replace(': ', '：')
        vidname = vidname.replace('"', '＂')
        Mp4 = vidname + ".mp4"
        Mp3 = vidname + ".mp3"
        Video = VideoFileClip(Mp4)
        Audio = Video.audio
        try:
            os.chdir(os.path.join(self.cwd, 'playlist'))
        except:
            os.mkdir(os.path.join(self.cwd, 'playlist'))
            os.chdir(os.path.join(self.cwd, 'playlist'))
        Audio.write_audiofile(Mp3)
        os.chdir(self.cwd)
        Audio.close()
        Video.close()
        os.remove(Mp4)
        data = SpotifyAPI.get_metadata(vidname)
        try:
            df = pd.read_csv(os.path.join(self.cwd, "metadata", "MusicData.csv"), encoding='utf-8')
            if len(data["artists"]) <= 1:
                data["artists"].append('')
            df.loc[len(df.index)] = [data["audio_features"]["id"], data["name"],
                                     data["artists"][0] + " | " + data["artists"][1], data["album"],
                                     data["year"], data["popularity"],
                                     data["audio_features"]["danceability"], data["audio_features"]["energy"],
                                     data["audio_features"]["key"], data["audio_features"]["loudness"],
                                     data["audio_features"]["mode"], data["audio_features"]["speechiness"],
                                     data["audio_features"]["acousticness"],
                                     data["audio_features"]["instrumentalness"],
                                     data["audio_features"]["liveness"], data["audio_features"]["valence"],
                                     data["audio_features"]["tempo"], data["audio_features"]["duration_ms"],
                                     data["audio_features"]["time_signature"]]
            df.to_csv(os.path.join(self.cwd, "metadata", "MusicData.csv"), index=False, encoding='utf-8')
        except:
            os.mkdir(os.path.join(self.cwd, "metadata"))
            df = open(os.path.join(self.cwd, "metadata", "MusicData.csv"), 'a', encoding='utf-8')
            temp_file = open(os.path.join(self.cwd, "metadata", "recommended_songs.txt") ,'a', encoding='utf-8')
            temp_file.close()
            df.write("id,name,artists,album,year,popularity,danceability,energy,key,loudness,"
                     "mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,duration_ms,"
                     "time_signature\n")
            if len(data["artists"]) <= 1:
                data["artists"].append('')
            df.write(data["audio_features"]["id"] + "," + data["name"] + "," +
                     data["artists"][0] + " | " + data["artists"][1] + "," +
                     data["album"] + "," + data["year"] + "," +
                     str(data["popularity"]) + ","+
                     str(data["audio_features"]["danceability"]) + "," +
                     str(data["audio_features"]["energy"]) + "," +
                     str(data["audio_features"]["key"]) + "," +
                     str(data["audio_features"]["loudness"]) + "," +
                     str(data["audio_features"]["mode"]) + "," +
                     str(data["audio_features"]["speechiness"]) + "," +
                     str(data["audio_features"]["acousticness"]) + "," +
                     str(data["audio_features"]["instrumentalness"]) + "," +
                     str(data["audio_features"]["liveness"]) + "," +
                     str(data["audio_features"]["valence"]) + "," +
                     str(data["audio_features"]["tempo"]) + "," +
                     str(data["audio_features"]["duration_ms"]) + "," +
                     str(data["audio_features"]["time_signature"]) + "\n")
            df.close()
        f = open(os.path.join(self.cwd, "playlist", "musicfiles.txt"), "a", encoding='utf-8')
        f1 = open(os.path.join(self.cwd, "playlist", "queue.txt"), "w", encoding='utf-8')
        f.write(Mp3 + '\n')
        f.close()
        mixer.music.stop()
        mixer.music.unload()
        return Mp3
@app.route("/sr", methods=["POST"])
def ind():
     global user_input ,result,l
     user_input= flask.request.form.get('song_name')
     result=queue.proc(user_input)
     l=[]
     for i in result[:4]:
         i = ((str(i).split("="))[-1])[0:-1]
         l.append((queue.name('https://www.youtube.com/watch?v='+i)))
     return render_template("search.html",options=l)
@app.route("/home")
def home():
     return render_template("homepage.html")
@app.route("/about")
def abt():
     return render_template("about.html")
@app.route("/pl")
def play():
    try:
        f = open("playlist\musicfiles.txt", "r", encoding='utf-8')
        f2=pd.read_csv("metadata\MusicData.csv",encoding='utf-8')
        r = f.readlines()
        a=[]
        for i in range(len(r)):
            a.append(f2.iloc[i]["name"]+" , "+f2.iloc[i]["artists"])
        return render_template("player.html",options=a)
    except:
        a="Playlist is empty"
        return render_template("error.html",error=a)
@app.route("/download",methods=["POST"])
def play1():
        choice = flask.request.form.get('songs')
        for i in range(len(l)):
            if l[i]==choice:
                choice=result[i]
                break
        song=queue.search(choice,user_input)
        queue.inputer()
        queue.playcurr(song)
        time.sleep(5)
        queue.play()
        f = open("playlist\musicfiles.txt", "r", encoding='utf-8')
        os.chdir(queue.cwd)
        f2=pd.read_csv("metadata\MusicData.csv",encoding='utf-8')
        r = f.readlines()
        a=[]
        for i in range(len(r)):
            a.append(f2.iloc[i]["name"]+" , "+f2.iloc[i]["artists"])
        return render_template("player.html",options=a)
@app.route("/recom")
def reco():
    try:
        Recommender.write_recommended()
        f = open("metadata/recommended_songs.txt", "r")
        r = f.readlines()
        return render_template("rec.html",options=r)
    except:
        return render_template("error.html",error="Your Ensou experience is 0\n try adding some songs to your playlist")
@app.route("/recdownload")
def download():
    text = flask.request.args.get('text', '')
    result=queue.proc(text)
    song=queue.search(result[0],text)
    f=open("playlist\queue.txt","w", encoding='utf-8')
    f.write(song+'\n')
    f.close()
    queue.temp_inputer()
    queue.play()
@app.route("/lyric")
def lyrics():
    text=queue.l.start.linker
    f=open("playlist\lyrics.txt","r", encoding='utf-8')
    f1=open("playlist\musicfiles.txt","r", encoding='utf-8')
    f2=pd.read_csv("metadata\MusicData.csv",encoding='utf-8')
    r=f1.readlines()
    r1=f.readlines()
    print(text)
    print(r1[0])
    for i in range(len(r)):
        if(text==r[i]):
            name=f2.iloc[i]['name']
            artist=f2.iloc[i]['artists']
            l=r1[i]
            break
    print(l)
    f1.close()
    f.close()
    return render_template("lyrics.html",options=l,song=name,artists=artist)
@app.route("/playcurr")
def cur():
    text = flask.request.args.get('text', '')
    f = open("playlist\musicfiles.txt", "r", encoding='utf-8')
    f2=pd.read_csv("metadata\MusicData.csv",encoding='utf-8')
    r = f.readlines()
    for i in range(len(r)):
        if str(f2.iloc[i]['name']) in text:
            text=r[i]
            print(text,"hjbhj")
    queue.playcurr(text)
    queue.play()
    a=[]
    for i in range(len(r)):
            a.append(f2.iloc[i]["name"]+" , "+f2.iloc[i]["artists"])
    print(text)
    return render_template("player.html",options=a)
@app.route("/repe")
def reper():
    print(queue.repeat)
    queue.repeater()
@app.route("/norepe")
def nrepe():
    queue.norep()
@app.route("/play")
def player():
    queue.inputer()
    queue.play()
    return render_template("player.html")
@app.route("/prev")
def preve():
    queue.prev()
@app.route("/next")
def nex():
    queue.next1()
@app.route("/pau")
def paus():
    queue.pause()
@app.route("/unpau")
def unpaus():
    queue.unpause()
if __name__ == "__main__":
    queue=MusicPlayer()
    app.run(debug=True)
