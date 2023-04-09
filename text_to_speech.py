# -*- coding: utf-8 -*-
import pyvcroid2
import threading
import time
import winsound
import sys
import wave
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
audio = pyaudio.PyAudio()
RATE = 44100
FILE_PATH = "voiceroid.wav"

DEFAULT_PARAMS={
    "volume":1,
    "speed":1,
    "pitch":1,
    "emphasis":1,
    "pause_middle":50,
    "pause_long":100,
    "pause_sentence":200,
    "master_volume":1,
}
def get_list():
    with pyvcroid2.VcRoid2() as vc: 
        voice_list = vc.listVoices()
        if 0 < len(voice_list):
            return voice_list
            
        else:
            raise Exception("No voice library")


def speech(message="default",chara = 0,params = DEFAULT_PARAMS):
    with pyvcroid2.VcRoid2() as vc:
        # Load language library
        lang_list = vc.listLanguages()
        try:
            if "standard" in lang_list:
                vc.loadLanguage("standard")
            elif 0 < len(lang_list):
                vc.loadLanguage(lang_list[0])
            else:
                raise Exception("No language library")
        except:       
            print("lang_list = ",lang_list)             
            print(sys.exc_info())
            return 

        
        # Load Voice
        voice_list = vc.listVoices() 
        vc.loadVoice(voice_list[chara])
        
        #print(voice_list[chara])
    
        vc.param.volume = params["volume"]
        vc.param.speed = params["speed"]
        vc.param.pitch = params["pitch"]
        vc.param.emphasis = params["emphasis"]
        vc.param.pauseMiddle = params["pause_middle"]
        vc.param.pauseLong = params["pause_long"]
        vc.param.pauseSentence = params["pause_sentence"]
        vc.param.masterVolume = params["master_volume"]
    
        # Text to speech
        speech, tts_events = vc.textToSpeech(message)

        wav = wave.open(FILE_PATH, 'wb')
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(audio.get_sample_size(FORMAT))
        wav.setframerate(RATE)
        wav.writeframes(speech)
        wav.close()

        winsound.PlaySound(FILE_PATH, winsound.SND_ASYNC)
        return tts_events
        
if __name__ == '__main__':
    text = input("text:")
    while text != "EXIT":
        speech(text)
        text = input("text:")
