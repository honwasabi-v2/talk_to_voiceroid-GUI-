
import threading
import tkinter as tk
import tkinter.ttk as ttk
import json
from importlib import import_module
import speech_to_text as stt
import text_to_speech as tts
import time

class w_talk:
    def __init__(self,master):
        config = load_config("config.json")
        self.params = config["paramater"]
        print(self.params)
        self.master = master        
        module_api = import_module(config["api"])
        self.API = module_api.api(config["key"][config["api"]])
        self.flag_rec = False
        self.flag_free = True
        self.thread_mic = None  
        self.thread_say = None
        self.num_char = 0
        self.kuchipaku = True
        
        #paramater_display 1~7
        self.var_volume = tk.DoubleVar()    
        self.var_volume.set(self.params["volume"])
        self.name_volume = tk.Label(master, text="volume")    
        self.param_volume = tk.Label(master, text=self.params["volume"])
        self.scale_volume = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=3, 
            resolution = 0.01,
            variable = self.var_volume,
            command=self.setter_volume,
            showvalue=False
            )
        self.scale_volume.grid(column=2, row=0, padx=10, pady=10)
        self.name_volume.grid(column=3, row=0, padx=10, pady=10)
        self.param_volume.grid(column=4, row=0, padx=10, pady=10)

        self.var_speed = tk.DoubleVar()    
        self.var_speed.set(self.params["speed"])
        self.name_speed = tk.Label(master, text="speed")    
        self.param_speed = tk.Label(master, text=self.params["speed"])
        self.scale_speed = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.var_speed,
            command=self.setter_speed,
            showvalue=False
            )
        self.scale_speed.grid(column=2, row=1, padx=10, pady=10)
        self.name_speed.grid(column=3, row=1, padx=10, pady=10)
        self.param_speed.grid(column=4, row=1, padx=10, pady=10)

        self.var_pitch = tk.DoubleVar()    
        self.var_pitch.set(self.params["pitch"])
        self.name_pitch = tk.Label(master, text="pitch")    
        self.param_pitch = tk.Label(master, text=self.params["pitch"])
        self.scale_pitch = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.var_pitch,
            command=self.setter_pitch,
            showvalue=False
            )
        self.scale_pitch.grid(column=2, row=2, padx=10, pady=10)
        self.name_pitch.grid(column=3, row=2, padx=10, pady=10)
        self.param_pitch.grid(column=4, row=2, padx=10, pady=10)

        self.var_emphasis = tk.DoubleVar()    
        self.var_emphasis.set(self.params["emphasis"])
        self.name_emphasis = tk.Label(master, text="emphasis")    
        self.param_emphasis = tk.Label(master, text=self.params["emphasis"])
        self.scale_emphasis = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.var_emphasis,
            command=self.setter_emphasis,
            showvalue=False
            )
        self.scale_emphasis.grid(column=2, row=3, padx=10, pady=10)
        self.name_emphasis.grid(column=3, row=3, padx=10, pady=10)
        self.param_emphasis.grid(column=4, row=3, padx=10, pady=10)

        self.var_pause_m = tk.IntVar()    
        self.var_pause_m.set(self.params["pause_middle"])
        self.name_pause_m = tk.Label(master, text="pause_middle")    
        self.param_pause_m = tk.Label(master, text=self.params["pause_middle"])
        self.scale_pause_m = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=200, 
            resolution = 0.01,
            variable = self.var_pause_m,
            command=self.setter_pause_m,
            showvalue=False
            )
        self.scale_pause_m.grid(column=2, row=4, padx=10, pady=10)
        self.name_pause_m.grid(column=3, row=4, padx=10, pady=10)
        self.param_pause_m.grid(column=4, row=4, padx=10, pady=10)

        self.var_pause_l = tk.IntVar()    
        self.var_pause_l.set(self.params["pause_long"])
        self.name_pause_l = tk.Label(master, text="pause_long")    
        self.param_pause_l = tk.Label(master, text=self.params["pause_long"])
        self.scale_pause_l = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=500, 
            resolution = 0.01,
            variable = self.var_pause_l,
            command=self.setter_pause_l,
            showvalue=False
            )
        self.scale_pause_l.grid(column=2, row=5, padx=10, pady=10)
        self.name_pause_l.grid(column=3, row=5, padx=10, pady=10)
        self.param_pause_l.grid(column=4, row=5, padx=10, pady=10)

        self.var_pause_s = tk.IntVar()    
        self.var_pause_s.set(self.params["pause_sentence"])
        self.name_pause_s = tk.Label(master, text="pause_sentence")    
        self.param_pause_s = tk.Label(master, text=self.params["pause_sentence"])
        self.scale_pause_s = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=1000, 
            resolution = 0.01,
            variable = self.var_pause_s,
            command=self.setter_pause_s,
            showvalue=False
            )
        self.scale_pause_s.grid(column=2, row=6, padx=10, pady=10)
        self.name_pause_s.grid(column=3, row=6, padx=10, pady=10)
        self.param_pause_s.grid(column=4, row=6, padx=10, pady=10)

        self.var_volume_m = tk.DoubleVar()    
        self.var_volume_m.set(self.params["master_volume"])
        self.name_volume_m = tk.Label(master, text="master_volume")    
        self.param_volume_m = tk.Label(master, text=self.params["master_volume"])
        self.scale_volume_m = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0.1,to=3, 
            resolution = 0.01,
            variable = self.var_volume_m,
            command=self.setter_volume_m,
            showvalue=False
            )
        self.scale_volume_m.grid(column=2, row=7, padx=10, pady=10)
        self.name_volume_m.grid(column=3, row=7, padx=10, pady=10)
        self.param_volume_m.grid(column=4, row=7, padx=10, pady=10)

        self.var_chars = tk.IntVar()    
        self.var_chars.set(self.num_char)
        self.name_chars = tk.Label(master, text="charctors")    
        self.label_num_char = tk.Label(master, text=self.num_char)
        self.scale_char = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=len(tts.get_list())-1, 
            resolution = 1,
            variable = self.var_chars,
            command=self.setter_char,
            showvalue=False
            )
        self.scale_char.grid(column=2, row=8, padx=10, pady=10)
        self.name_chars.grid(column=3, row=8, padx=10, pady=10)
        self.label_num_char.grid(column=4, row=8, padx=10, pady=10)

        self.var_kuchipaku = tk.IntVar()    
        self.var_kuchipaku.set(1)
        self.name_kuchipaku = tk.Label(master, text="口パク")    
        self.label_num_kuchipaku = tk.Label(master, text="ON")
        self.scale_kuchipaku = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_ = 0,to=1, 
            resolution = 1,
            variable = self.var_kuchipaku,
            command=self.chenge_kuchipaku,
            showvalue=False
            )
        self.scale_kuchipaku.grid(column=2, row=9, padx=10, pady=10)
        self.name_kuchipaku.grid(column=3, row=9, padx=10, pady=10)
        self.label_num_kuchipaku.grid(column=4, row=9, padx=10, pady=10)
        

        #image load & resize
        self.tachie_close=tk.PhotoImage(file=config["figure"]["close"])
        self.tachie_close=resize_image(self.tachie_close)        
        self.tachie_half=tk.PhotoImage(file=config["figure"]["half"])
        self.tachie_half=resize_image(self.tachie_half)     
        self.tachie_open=tk.PhotoImage(file=config["figure"]["open"])
        self.tachie_open=resize_image(self.tachie_open)
                        
        self.canvas=tk.Canvas(master,bg="BLACK", width=300, height=400)
        self.canvas.grid(column=0,columnspan=1, row=0, rowspan=5,padx=10, pady=10)
        self.canvas.create_image(0, 0, image=self.tachie_open, anchor=tk.NW,tag = "open")
        self.canvas.create_image(0, 0, image=self.tachie_half, anchor=tk.NW,tag = "half")
        self.canvas.create_image(0, 0, image=self.tachie_close, anchor=tk.NW,tag = "close")
        
        #keyboard input
        self.txtbox = tk.Text(master,width=80,height =15)
        self.txtbox.grid(column=0,columnspan=2,row=6,  rowspan=3,padx=10, pady=10)
        self.button_send = tk.Button(
            master,
            text="送信",
            command = self.send_KB
            )
        self.button_send.grid(column=0, row=10, padx=10, pady=10)

        #reply text
        self.reply = tk.Text(master,height =30,width=30,state = tk.NORMAL)
        self.reply.grid(column=1,columnspan=1, row=0, rowspan=5,padx=10, pady=10)

        #mode chenge recording
        self.button_rec = tk.Button(
            master,
            text="録音開始",
            command = self.rec_chenge
            )
        self.button_rec.grid(column=1, row=10, padx=10, pady=10)

    def setter_volume(self,event=None):
        self.params["volume"] = self.var_volume.get()
        self.param_volume["text"] = self.params["volume"]
    def setter_speed(self,event=None):
        self.params["speed"] = self.var_speed.get()
        self.param_speed["text"] = self.params["speed"]
    def setter_pitch(self,event=None):
        self.params["pitch"] = self.var_pitch.get()
        self.param_pitch["text"] = self.params["pitch"]
    def setter_emphasis(self,event=None):
        self.params["emphasis"] = self.var_emphasis.get()
        self.param_emphasis["text"] = self.params["emphasis"]  
    def setter_pause_m(self,event=None):
        self.params["pause_middle"] = self.var_pause_m.get()
        self.param_pause_m["text"] = self.params["pause_middle"]
        if self.params["pause_middle"] > self.params["pause_long"]:
            self.params["pause_long"] = self.params["pause_middle"]
            self.var_pause_l.set(self.params["pause_long"])
            self.param_pause_l["text"] = self.params["pause_long"]
            if self.params["pause_middle"] > self.params["pause_sentence"]:
                self.params["pause_sentence"] = self.params["pause_middle"]
                self.var_pause_s.set(self.params["pause_sentence"])
                self.param_pause_s["text"] = self.params["pause_sentence"]
    def setter_pause_l(self,event=None):
        self.params["pause_long"] = self.var_pause_l.get()
        self.param_pause_l["text"] = self.params["pause_long"]
        if self.params["pause_long"] < self.params["pause_middle"]:
            self.params["pause_middle"] = self.params["pause_long"]
            self.var_pause_m.set(self.params["pause_middle"])
            self.param_pause_m["text"] = self.params["pause_middle"]
        if self.params["pause_long"] > self.params["pause_sentence"]:
            self.params["pause_sentence"] = self.params["pause_long"]
            self.var_pause_s.set(self.params["pause_sentence"])
            self.param_pause_s["text"] = self.params["pause_sentence"]
    def setter_pause_s(self,event=None):
        self.params["pause_sentence"] = self.var_pause_s.get()
        self.param_pause_s["text"] = self.params["pause_sentence"]

        if self.params["pause_sentence"] < self.params["pause_long"]:
            self.params["pause_long"] = self.params["pause_sentence"]
            self.var_pause_l.set(self.params["pause_long"])
            self.param_pause_l["text"] = self.params["pause_long"]
            if self.params["pause_sentence"] < self.params["pause_middle"]:
                self.params["pause_middle"] = self.params["pause_sentence"]
                self.var_pause_m.set(self.params["pause_middle"])
                self.param_pause_m["text"] = self.params["pause_middle"]     
    def setter_volume_m(self,event=None):
        self.params["master_volume"] = self.var_volume_m.get()
        self.param_volume_m["text"] = self.params["master_volume"]
    def setter_char(self,event=None):
        self.num_char = self.var_chars.get()
        self.label_num_char["text"] = self.num_char  
    def chenge_kuchipaku(self,event=None):
        if(self.var_kuchipaku.get() == 1):
            self.label_num_kuchipaku["text"] = "ON"
            self.kuchipaku = True
        elif(self.var_kuchipaku.get() == 0): 
            self.label_num_kuchipaku["text"] = "OFF"
            self.kuchipaku = False
        else:
            self.label_num_kuchipaku["text"] = "Err"
            self.kuchipaku = True
    def send_KB(self,event=None):
        if self.flag_free and not(self.flag_rec):
            self.flag_free = False
            message = self.txtbox.get(0., tk.END)
            message = message.replace('\n','')
            self.talk(message,mause=self.kuchipaku)
            self.txtbox.delete(0., tk.END)
            self.flag_free = True
        else:
            print("now doing")
    
    def rec_chenge(self,event=None):
        if self.flag_rec:
            print("push 録音終了")
            self.flag_rec = False
            self.txtbox["state"] = tk.NORMAL
            self.button_rec["text"] = "録音開始"
        else:
            print("push 録音開始")
            self.flag_rec = True
            self.txtbox.delete(0.,tk.END)
            self.txtbox["state"] = tk.DISABLED
            self.button_rec["text"] = "録音終了"
            self.thread_mic = threading.Thread(target=self.thf1_mic,daemon=True)
            self.thread_mic.start()

    def thf1_mic(self):     #thread function
        while self.flag_rec:
            self.flag_free  = False
            stt.recording()
            text=stt.wav_to_text("output.wav")
            print(text)
            time_wait = self.talk(text,mause=self.kuchipaku)
            self.flag_free  = True     
            time.sleep(time_wait*0.001)          
        else:
            print("flag_rec is False")

    def send_text(self,text):   #Forming sentences to be sent to the API
        if text != "" and text != "\r\n\ " :
            reply = self.API.send(text)
            return reply
        else:
            if self.flag_rec:
                return ""
            else:
                return "何か入力してください"  

    def talk(self,text,mause = True):    
        #textarea write&say&kuchipaku
        #paramater mause is kuchipaku,default ON 
        reply=self.send_text(text)
        print(reply)
        if reply == "":
            print("no reply")
            return 0
        textarea_write(self.reply,reply)
        self.change_image("open")
        events = tts.speech(message = reply,chara=self.num_char,params=self.params)  
        if mause:
            for itr in events:
                if itr[2] == "a" or itr[2] == "e":
                    self.canvas.after(itr[0],self.change_image,"open")
                elif itr[2] == "i"or itr[2] == "u"or itr[2] == "o":
                    self.canvas.after(itr[0],self.change_image,"half")
                elif itr[2] == "N":
                    self.canvas.after(itr[0],self.change_image,"close")
        time = next(iter(reversed(events)))[0]
        self.canvas.after(time,self.change_image,"close")
        return time


    def change_image(self,tag):
        self.canvas.lift(tag)
        self.canvas.update()

def resize_image(image):
    if image.width() > 300 or image.height() > 400:
        if image.width()/300 > image.height()/400:
            rate = image.width()/300+1
        else:
            rate = image.height()/400+1
        
        return image.subsample(int(rate))
    else:
        print("height=",image.height())
        if image.width()/300 > image.height()/400:
            rate = image.width()/300+1
        else:
            rate = image.height()/400+1
            
        return image.zoom(int(rate))

def load_config(filename):
    file = open(filename, 'r')
    config = json.load(file)
    return config

def textarea_write(text_area,str):
    text_area.delete(0.,tk.END)
    text_area.insert(0.,str)
    text_area.update()


root = tk.Tk()
root.title('talk')
root.geometry('1000x800')
window = w_talk(root)
root.mainloop()
