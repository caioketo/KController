from gmusicapi import Webclient
from gplayer import Player
from pprint import pprint
import telnetlib
import operator
import collections

class Playlist:
    def __init__(self):
        self.songs = []
        self.name = ''
        self.id = ''
        self.index = -1

class Song:
    def __init__(self):
        self.id = ""

    def __eq__(self, other):
        return self.id == other.id
   
    def __ne__(self, other):
        return not self.id == other.id    

    def __cmp__(self, other):
        if self.id < other.id:  # compare name value (should be unique)
            return -1
        elif self.id > other.id:
            return 1
        else: return 0


class Album:
    id = -1
    url = ""
    def __init__(self):
        self.name = ""
        self.url = ""
        self.songs = []
        self.artistId = -1

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.name == other.name

    def __cmp__(self, other):
        if self.name < other.name:  # compare name value (should be unique)
            return -1
        elif self.name > other.name:
            return 1
        else: return 0

class Artist:
    id = -1
    def __init__(self):
        self.name = ""
        self.url = ""
        self.albums = []

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.name == other.name
    
    def __cmp__(self, other):
        if self.name < other.name:  # compare name value (should be unique)
            return -1
        elif self.name > other.name:
            return 1
        else: return 0

class Gmusic:
    artists = []
    playlists = []
    api = Webclient()
    player = Player(api)

    def telnetCmd(self, cmd):
        tn = telnetlib.Telnet('localhost', '6600')
        tn.read_until('OK MPD 0.16.0')
        tn.write(cmd + "\n")
        result = tn.read_until('OK', 10)
        tn.close()
        return result

    def playSong(self, songId):
        url = self.api.get_stream_urls(songId)[0]
        self.telnetCmd('clear')
        self.telnetCmd('add ' + str(url))
        self.telnetCmd('play')

    def playList(self, playlistId):
        self.player.setPlaylist(self.playlists[playlistId])
        self.player.playSong()
 
    def login(self):
        usuario = 'caionmoreno1@gmail.com'
        senha = 'vd001989'
        loggedin = Gmusic.api.login(usuario, senha)
        return loggedin
    
    def loadSongs(self):
        songsApi = Gmusic.api.get_all_songs()
        for s in songsApi:
            artistC = Artist()
            artistC.name = s["artist"]
            artistC.url = s.get('artistImageBaseUrl', '')
            artistIndex = -1
            if not (artistC in self.artists):
                artistC.id = len(Gmusic.artists)
                artistIndex = artistC.id
                self.artists.append(artistC)
            else:
                artistIndex = self.artists.index(artistC)
            
            albumC = Album()
            albumC.name = s["album"]
            albumC.url = s.get('albumArtUrl', '')
            albumC.artistId = self.artists[artistIndex].id
            if not (albumC in self.artists[artistIndex].albums):
                albumC.id = len(self.artists[artistIndex].albums)
                self.artists[artistIndex].albums.append(albumC)
                albumIndex = albumC.id
            else:
                albumIndex = self.artists[artistIndex].albums.index(albumC)

            song = Song()
            song.id = s["id"]
            song.title = s["title"]
            self.artists[artistIndex].albums[albumIndex].songs.append(song)


    def loadPlaylists(self):
        plApi = Gmusic.api.get_all_playlist_ids()
        for name,pids in plApi['user'].iteritems():
            for pid in pids:
                playlist = Playlist()
                playlist.name = name
                playlist.id = pid
                playlist.index = len(self.playlists)
                tracks = self.api.get_playlist_songs(pid)
                for s in tracks:
                    song = Song()
                    song.id = s["id"]
                    song.title = s["title"]
                    song.album = s["album"]
                    song.artist = s["artist"]
                    playlist.songs.append(song)
                self.playlists.append(playlist)

    def __init__(self):
        a = ""
