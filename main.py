import copy
import os
from time import sleep

from mutagen.mp3 import MP3

import googleInteraction

import config # this is a file that sets the environmental variables

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

from playsound import playsound

results = sp.current_playback()

class currentPlaybackObject:
    results = sp.current_playback()
    currentTime = results['progress_ms']
    duration = results['item']['duration_ms']
    title = results["item"]['name']
    artist = results["item"]['artists'][0]['name']
    def refresh(self):
        self.results = sp.current_playback()
        self.currentTime = self.results['progress_ms']
        self.duration = self.results['item']['duration_ms']
        self.title = self.results["item"]['name']
    def getTrack(self):
        self.refresh()
        return results['item']['id']
    def getFadeOut(self):
        self.refresh()
        audioAnalysis = sp.audio_analysis(self.getTrack())
        return audioAnalysis['track']['start_of_fade_out']
    def getRemainingTime(self):
        self.refresh()
        fadeOut = self.getFadeOut()
        return (fadeOut - self.results['progress_ms'] / 1000)
    def getDuration(self):
        self.refresh()
        return self.duration
    def getResults(self):
        return self.results
    def getCurrentName(self):
        self.refresh()
        return self.title
    def getCurrentArtist(self):
        self.refresh()
        return self.artist

cp = currentPlaybackObject()
while True:
    remainingTime = cp.getRemainingTime()
    if (remainingTime > 30):
        #since there is over 30 seconds left in the song, sleep 28 seconds and then check again
        sleep(28)
    remainingTime = cp.getRemainingTime()
    if (remainingTime < 30):
        print(cp.getTrack() + " track 1 st time")
        print(str(remainingTime) + "left")
        cp.refresh()
        #create the voice track
        results = cp.getResults()
        spokenString = "That was " + results["item"]['name'] + " by " + results["item"]['artists'][0]['name']
        googleInteraction.synthesizeText(spokenString, "ending.mp3")
        voiceTrack = MP3("ending.mp3")
        print("voicetrack length: " + str(voiceTrack.info.length))
        #special start here
        finishingTitle = copy.deepcopy(cp.getCurrentName())
        if(remainingTime-voiceTrack.info.length) > 0:
            sleep(remainingTime-voiceTrack.info.length)
        print(spokenString)
        playsound("ending.mp3")
        while (cp.getCurrentName() == finishingTitle):
            remainingTime = cp.getRemainingTime()
            print("remaining time:")
            print(remainingTime)
            if remainingTime > 0:
                sleep(remainingTime)
            cp.refresh()
        spokenString = "Now here is" + cp.getCurrentName() + " by " + cp.getCurrentArtist()
        print(spokenString)
        googleInteraction.synthesizeText(spokenString, "beginning.mp3")
        playsound("beginning.mp3")