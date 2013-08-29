import threading
import mpc
import time
from gmusicapi import Api
from random import randint

class PlayerUpdate(threading.Thread):
    def __init__(self, player):
        self.__player = player
        self.__name = "Playlist Updater"
        self.__running = True
        threading.Thread.__init__(self)
    
    def setRunning(self, running):
        self.__running = running        
        
    def run(self):
        while(self.__running):
            current = mpc.sysCmd('mpc current')
            if(len(current.strip()) == 0):
                next = self.__player.next()
                if next is None:
                    self.__running = False
                else:
                    url = Player.api.get_stream_urls(next)[0]
                    mpc.telnetCmd('clear')
                    mpc.telnetCmd('add ' + str(url))
                    mpc.telnetCmd('play')    
            time.sleep(3)

class Player(object):
    api = None
    updater = None
    current = None
    playlist = None
    random = False
    
    def __init__(self, a): 
        Player.api = a
        Player.updater = PlayerUpdate(self)
        Player.random = True
        
    def getCurrentSong(self):
        return Player.current;
    
    def setPlaylist(self, pl):
        self.stop()
        Player.playlist = pl
        
    def stop(self):
        Player.updater.setRunning(False)
        mpc.telnetCmd('clear')
        mpc.telnetCmd('stop')
        return str(True);
        
    def next(self):
        index = 0
        if Player.playlist is None:
            return None
            
        if Player.random:
            index = randint(0, len(Player.playlist.songs))
        else:
            for track in Player.playlist.songs:
                if(track.id != Player.current):
                    index+=1
                else:
                    break
            index+=1            
        if index < len(Player.playlist):
            Player.current = Player.playlist.songs[index].id
        else:
            Player.current = None
        return Player.current
        
    def previous(self):
        index = 0
        if Player.playlist is None:
            return None
            
        for track in Player.playlist.songs:
            if(track.id != Player.current):
                index+=1;
            else:
                break
                
        index-=1
        if index >= 0:
            Player.current = Player.playlist.songs[index].id
        else:
            Player.current = Player.playlist.songs[0].id
        return Player.current
        
            
    def playSong(self, songId=None):
        self.stop()
        
        if(songId is None):
            Player.current = Player.playlist.songs[0].id
        else:
            Player.current = songId;
            
        url = Player.api.get_stream_urls(Player.current)[0]
        mpc.telnetCmd('clear')
        mpc.telnetCmd('add ' + str(url))
        mpc.telnetCmd('play')
        
        Player.updater = PlayerUpdate(self)
        Player.updater.setRunning(True)
        Player.updater.start()
            
        return Player.current
