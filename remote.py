#!/usr/bin/env python

from lirc.lirc import Lirc
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from canais import Canais
from gmusic import Gmusic
from pprint import pprint
import time

BASE_URL = ''

app = Flask(__name__)

# Initialise the Lirc config parser
lircParse = Lirc('/etc/lirc/lircd.conf')
gmusic = Gmusic()
gmusic.login()
gmusic.loadSongs()
gmusic.loadPlaylists()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/canais")
def canais():
    canais = []
    ccanais = Canais()
    for can in ccanais.getCanais():
        c = {'numero': can.numero, 'canal': can.canal,}
        canais.append(c)
    return render_template('canais.html', canais=canais)


@app.route("/canal/<numero>")
def clicked(numero=None):
    # Send message to Lirc to control the IR
    for c in numero:
        key = "KEY_" + c
        lircParse.send_once("gvt", key)
        time.sleep(1)
   
    lircParse.send_once("gvt", "KEY_OK")
    return ""

@app.route("/volume/<vol>")
def clickedd(vol=None):
    if (vol == "UP"):
        lircParse.send_once("gvt", "KEY_VOLUMEUP")
    else:
        lircParse.send_once("gvt", "KEY_VOLUMEDOWN")
    return ""

@app.route("/playmusic/<musicId>")
def playMusic(musicId=None):
    if (musicId != None):
        gmusic.playSong(musicId)
    return ""

@app.route("/playlist/<plId>")
def playList(plId=None):
    if (plId != None):
        gmusic.playList(int(plId))
    return ""

@app.route("/musics/<artist>,<album>")
def musicList(artist=None,album=None):
    if (album != None):
        return render_template('musics.html', musics=gmusic.artists[int(artist)].albums[int(album)].songs)

@app.route("/playlists")
def playlists():
    return render_template('playlists.html', playlists=gmusic.playlists)

@app.route("/artists/list")
def artistList():
    return render_template('artists.html', artists=gmusic.artists)

@app.route("/albums/<artist>")
def albumList(artist=None):
    if (artist != None):
        return render_template('albums.html', albums=gmusic.artists[int(artist)].albums)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')


