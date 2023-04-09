# -*- coding: utf-8 -*-


import pyaudio
import wave
import speech_recognition as sr

import numpy as np
import time 

FILE_PATH = "output.wav"
    


def recording():    
    # 音データフォーマット
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    audio = pyaudio.PyAudio()
    RATE = 44100
    
    SILENT = 0.3    #無音終了時間
    threshold = 0.1 # 閾値 
    
    print("recording......")
    
    #話しし始めるまでループ
    while True:
       # 音の取込開始
       stream = audio.open(format = FORMAT,
          channels = CHANNELS,
          rate = RATE,
          input = True,
          frames_per_buffer = chunk
          )
       # 音データの取得
       data = stream.read(chunk)
       # ndarrayに変換
       x = np.frombuffer(data, dtype="int16") / 32768.0
    
       if x.max() > threshold:
          print("recording start")
          finish = False
          frames = []
          # 録音処理
          while True:        
              print("recording now...")
              for i in range(0, int(RATE / chunk * 1)):
                  data = stream.read(chunk)
                  frames.append(data)
                  ndarray = np.frombuffer(data, dtype="int16") / 32768.0
              if ndarray.max() < threshold:
                  zr = 0
                  while True:                
                      data = stream.read(chunk)
                      ndarray = np.frombuffer(data, dtype="int16") / 32768.0
                      if zr >= SILENT:
                          finish = True
                          break
                      if ndarray.max() > threshold:
                          zr = 0
                          #print(zr)
                          break
                      time.sleep(0.01)
                      zr += 0.01
                      #print(zr)
              if finish:
                  break
          break
    
    # 録音終了処理
    print("record finish")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # 録音データをファイルに保存
    wav = wave.open(FILE_PATH, 'wb')
    wav.setnchannels(CHANNELS)
    wav.setsampwidth(audio.get_sample_size(FORMAT))
    wav.setframerate(RATE)
    wav.writeframes(b''.join(frames))
    wav.close()
 
def wav_to_text(filename = FILE_PATH):
    r = sr.Recognizer()
     
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='ja-JP')
    except:
        print("上手く聞き取れませんでした")
        text = ""
    return text


if __name__ == "__main__":
    recording()
    text = wav_to_text(FILE_PATH)
    print("text = ",text)
    