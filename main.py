
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
        self.num_char = config["charactor"]
        self.lip =config["lip_sync"]
        self.config_window = None


                

        #image load & resize
        self.tachie_close=tk.PhotoImage(file=config["figure"]["close"])
        self.tachie_close=resize_image(self.tachie_close)        
        self.tachie_half=tk.PhotoImage(file=config["figure"]["half"])
        self.tachie_half=resize_image(self.tachie_half)     
        self.tachie_open=tk.PhotoImage(file=config["figure"]["open"])
        self.tachie_open=resize_image(self.tachie_open)
                        
        self.canvas=tk.Canvas(master,bg="BLACK", width=300, height=400)
        self.canvas.grid(column=0,columnspan=2, row=0, rowspan=1,padx=10, pady=10)
        self.canvas.create_image(0, 0, image=self.tachie_close, anchor=tk.NW,tag = "close")
 
        #reply text
        self.reply = tk.Text(
            master,
            height =30,width=30,
            state = tk.NORMAL
            )
        self.reply.grid(column=2,columnspan=2, row=0, rowspan=1,padx=10, pady=10)
        
        #keyboard input
        self.txtbox = tk.Text(master,width=80,height =15)
        self.txtbox.grid(column=0,columnspan=4,row=1,  rowspan=1,padx=10, pady=10)

        

        self.button_send = tk.Button(
            master,
            text="送信",
            command = self.send_KB
            )
        self.button_send.grid(column=0, row=2, padx=10, pady=10)

        #mode chenge recording
        self.button_rec = tk.Button(
            master,
            text="録音開始",
            command = self.rec_chenge
            )
        self.button_rec.grid(column=1, row=2, padx=10, pady=10)

        self.config_button = tk.Button(
            master,
            text = "config",
            command = self.create_config_window
            )
        self.config_button.grid(column=2, row=2, padx=10, pady=10) 



    def create_config_window(self,event= None):
        self.config_window = tk.Toplevel(self.master)
        self.config_window.title("config")
        self.config_window.geometry("300x450")
        #paramater_display 1~7
        self.config_window.var_volume = tk.DoubleVar()    
        self.config_window.var_volume.set(self.params["volume"])
        self.config_window.name_volume = tk.Label(self.config_window, text="volume")    
        self.config_window.param_volume = tk.Label(self.config_window, text=self.params["volume"])
        self.config_window.scale_volume = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=3, 
            resolution = 0.01,
            variable = self.config_window.var_volume,
            command=self.setter_volume,
            showvalue=False
            )
        self.config_window.scale_volume.grid(column=0, row=0, padx=10, pady=10)
        self.config_window.name_volume.grid(column=1, row=0, padx=10, pady=10)
        self.config_window.param_volume.grid(column=2, row=0, padx=10, pady=10)

    
        self.config_window.var_speed = tk.DoubleVar()    
        self.config_window.var_speed.set(self.params["speed"])
        self.config_window.name_speed = tk.Label(self.config_window, text="speed")    
        self.config_window.param_speed = tk.Label(self.config_window, text=self.params["speed"])
        self.config_window.scale_speed = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.config_window.var_speed,
            command=self.setter_speed,
            showvalue=False
            )
        self.config_window.scale_speed.grid(column=0, row=1, padx=10, pady=10)
        self.config_window.name_speed.grid(column=1, row=1, padx=10, pady=10)
        self.config_window.param_speed.grid(column=2, row=1, padx=10, pady=10)

        self.config_window.var_pitch = tk.DoubleVar()    
        self.config_window.var_pitch.set(self.params["pitch"])
        self.config_window.name_pitch = tk.Label(self.config_window, text="pitch")    
        self.config_window.param_pitch = tk.Label(self.config_window, text=self.params["pitch"])
        self.config_window.scale_pitch = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.config_window.var_pitch,
            command=self.setter_pitch,
            showvalue=False
            )
        self.config_window.scale_pitch.grid(column=0, row=2, padx=10, pady=10)
        self.config_window.name_pitch.grid(column=1, row=2, padx=10, pady=10)
        self.config_window.param_pitch.grid(column=2, row=2, padx=10, pady=10)

        self.config_window.var_emphasis = tk.DoubleVar()    
        self.config_window.var_emphasis.set(self.params["emphasis"])
        self.config_window.name_emphasis = tk.Label(self.config_window, text="emphasis")    
        self.config_window.param_emphasis = tk.Label(self.config_window, text=self.params["emphasis"])
        self.config_window.scale_emphasis = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=2, 
            resolution = 0.01,
            variable = self.config_window.var_emphasis,
            command=self.setter_emphasis,
            showvalue=False
            )
        self.config_window.scale_emphasis.grid(column=0, row=3, padx=10, pady=10)
        self.config_window.name_emphasis.grid(column=1, row=3, padx=10, pady=10)
        self.config_window.param_emphasis.grid(column=2, row=3, padx=10, pady=10)

        self.config_window.var_pause_m = tk.IntVar()    
        self.config_window.var_pause_m.set(self.params["pause_middle"])
        self.config_window.name_pause_m = tk.Label(self.config_window, text="pause_middle")    
        self.config_window.param_pause_m = tk.Label(self.config_window, text=self.params["pause_middle"])
        self.config_window.scale_pause_m = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=200, 
            resolution = 0.01,
            variable = self.config_window.var_pause_m,
            command=self.setter_pause_m,
            showvalue=False
            )
        self.config_window.scale_pause_m.grid(column=0, row=4, padx=10, pady=10)
        self.config_window.name_pause_m.grid(column=1, row=4, padx=10, pady=10)
        self.config_window.param_pause_m.grid(column=2, row=4, padx=10, pady=10)

        self.config_window.var_pause_l = tk.IntVar()    
        self.config_window.var_pause_l.set(self.params["pause_long"])
        self.config_window.name_pause_l = tk.Label(self.config_window, text="pause_long")    
        self.config_window.param_pause_l = tk.Label(self.config_window, text=self.params["pause_long"])
        self.config_window.scale_pause_l = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=500, 
            resolution = 0.01,
            variable = self.config_window.var_pause_l,
            command=self.setter_pause_l,
            showvalue=False
            )
        self.config_window.scale_pause_l.grid(column=0, row=5, padx=10, pady=10)
        self.config_window.name_pause_l.grid(column=1, row=5, padx=10, pady=10)
        self.config_window.param_pause_l.grid(column=2, row=5, padx=10, pady=10)

        self.config_window.var_pause_s = tk.IntVar()    
        self.config_window.var_pause_s.set(self.params["pause_sentence"])
        self.config_window.name_pause_s = tk.Label(self.config_window, text="pause_sentence")    
        self.config_window.param_pause_s = tk.Label(self.config_window, text=self.params["pause_sentence"])
        self.config_window.scale_pause_s = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=1000, 
            resolution = 0.01,
            variable = self.config_window.var_pause_s,
            command=self.setter_pause_s,
            showvalue=False
            )
        self.config_window.scale_pause_s.grid(column=0, row=6, padx=10, pady=10)
        self.config_window.name_pause_s.grid(column=1, row=6, padx=10, pady=10)
        self.config_window.param_pause_s.grid(column=2, row=6, padx=10, pady=10)

        self.config_window.var_volume_m = tk.DoubleVar()    
        self.config_window.var_volume_m.set(self.params["master_volume"])
        self.config_window.name_volume_m = tk.Label(self.config_window, text="master_volume")    
        self.config_window.param_volume_m = tk.Label(self.config_window, text=self.params["master_volume"])
        self.config_window.scale_volume_m = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0.1,to=3, 
            resolution = 0.01,
            variable = self.config_window.var_volume_m,
            command=self.setter_volume_m,
            showvalue=False
            )
        self.config_window.scale_volume_m.grid(column=0, row=7, padx=10, pady=10)
        self.config_window.name_volume_m.grid(column=1, row=7, padx=10, pady=10)
        self.config_window.param_volume_m.grid(column=2, row=7, padx=10, pady=10)

        self.config_window.var_lip_sync = tk.IntVar() 
        self.config_window.var_lip_sync.set(self.lip)
        self.config_window.name_lip_sync = tk.Label(self.config_window, text="口パク")    
        self.config_window.label_num_lip_sync = tk.Label(self.config_window, text=str(self.lip))
        self.config_window.scale_lip_sync = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=1, 
            resolution = 1,
            variable = self.config_window.var_lip_sync,
            command=self.setter_lip_sync,
            showvalue=False
            )
        self.config_window.scale_lip_sync.grid(column=0, row=9, padx=10, pady=10)
        self.config_window.name_lip_sync.grid(column=1, row=9, padx=10, pady=10)
        self.config_window.label_num_lip_sync.grid(column=2, row=9, padx=10, pady=10)


        self.config_window.var_chars = tk.IntVar()    
        self.config_window.var_chars.set(self.num_char)
        self.config_window.name_chars = tk.Label(self.config_window, text="charctors")    
        self.config_window.label_num_char = tk.Label(self.config_window, text=self.num_char)
        self.config_window.scale_char = tk.Scale(
            self.config_window,
            orient=tk.HORIZONTAL,
            from_ = 0,to=len(tts.get_list())-1, 
            resolution = 1,
            variable = self.config_window.var_chars,
            command=self.setter_char,
            showvalue=False
            )
        self.config_window.scale_char.grid(column=0, row=8, padx=10, pady=10)
        self.config_window.name_chars.grid(column=1, row=8, padx=10, pady=10)
        self.config_window.label_num_char.grid(column=2, row=8, padx=10, pady=10)



    def setter_volume(self,event=None):
        self.params["volume"] = self.config_window.var_volume.get()
        self.config_window.param_volume["text"] = self.params["volume"]
    def setter_speed(self,event=None):
        self.params["speed"] = self.config_window.var_speed.get()
        self.config_window.param_speed["text"] = self.params["speed"]
    def setter_pitch(self,event=None):
        self.params["pitch"] = self.config_window.var_pitch.get()
        self.config_window.param_pitch["text"] = self.params["pitch"]
    def setter_emphasis(self,event=None):
        self.params["emphasis"] = self.config_window.var_emphasis.get()
        self.config_window.param_emphasis["text"] = self.params["emphasis"]  
    def setter_pause_m(self,event=None):
        self.params["pause_middle"] = self.config_window.var_pause_m.get()
        self.config_window.param_pause_m["text"] = self.params["pause_middle"]
        if self.params["pause_middle"] > self.params["pause_long"]:
            self.params["pause_long"] = self.params["pause_middle"]
            self.config_window.var_pause_l.set(self.params["pause_long"])
            self.config_window.param_pause_l["text"] = self.params["pause_long"]
            if self.params["pause_middle"] > self.params["pause_sentence"]:
                self.params["pause_sentence"] = self.params["pause_middle"]
                self.config_window.var_pause_s.set(self.params["pause_sentence"])
                self.config_window.param_pause_s["text"] = self.params["pause_sentence"]
    def setter_pause_l(self,event=None):
        self.params["pause_long"] = self.config_window.var_pause_l.get()
        self.config_window.param_pause_l["text"] = self.params["pause_long"]
        if self.params["pause_long"] < self.params["pause_middle"]:
            self.params["pause_middle"] = self.params["pause_long"]
            self.config_window.var_pause_m.set(self.params["pause_middle"])
            self.config_window.param_pause_m["text"] = self.params["pause_middle"]
        if self.params["pause_long"] > self.params["pause_sentence"]:
            self.params["pause_sentence"] = self.params["pause_long"]
            self.config_window.var_pause_s.set(self.params["pause_sentence"])
            self.config_window.param_pause_s["text"] = self.params["pause_sentence"]
    def setter_pause_s(self,event=None):
        self.params["pause_sentence"] = self.config_window.var_pause_s.get()
        self.config_window.param_pause_s["text"] = self.params["pause_sentence"]

        if self.params["pause_sentence"] < self.params["pause_long"]:
            self.params["pause_long"] = self.params["pause_sentence"]
            self.config_window.var_pause_l.set(self.params["pause_long"])
            self.config_window.param_pause_l["text"] = self.params["pause_long"]
            if self.params["pause_sentence"] < self.params["pause_middle"]:
                self.params["pause_middle"] = self.params["pause_sentence"]
                self.config_window.var_pause_m.set(self.params["pause_middle"])
                self.config_window.param_pause_m["text"] = self.params["pause_middle"]     
    def setter_volume_m(self,event=None):
        self.params["master_volume"] = self.config_window.var_volume_m.get()
        self.config_window.param_volume_m["text"] = self.params["master_volume"]

    def setter_char(self,event=None):
        self.num_char = self.config_window.var_chars.get()
        self.config_window.label_num_char["text"] = self.num_char  


    def setter_lip_sync(self,event=None):
        self.lip = bool(self.config_window.var_lip_sync.get())
        self.config_window.label_num_lip_sync["text"] = str(self.lip)



    def send_KB(self,event=None):
        if self.flag_free and not(self.flag_rec):
            self.flag_free = False
            message = self.txtbox.get(0., tk.END)
            message = message.replace('\n','')
            self.talk(message,mouth=self.lip)
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
            time_wait = self.talk(text,mouth=self.lip)
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

    def talk(self,text,mouth = True):    
        #textarea write&say&lip_sync
        #paramater mouth is lip_sync,default ON 
        reply=self.send_text(text)
        print(reply)
        if reply == "":
            print("no reply")
            return 0
        textarea_write(self.reply,reply)
        self.change_image("open")
        events = tts.speech(message = reply,chara=self.num_char,params=self.params)  
        if mouth:
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
        #現在の画像を全て消す
        image_now_tag = self.canvas.find_all()
        self.canvas.delete(image_now_tag)

        #新しくtagに沿った画像をキャンバスに描く
        if tag == "open":
            self.canvas.create_image(0, 0, image=self.tachie_open, anchor=tk.NW,tag = "open")
        elif tag == "half":
            self.canvas.create_image(0, 0, image=self.tachie_half, anchor=tk.NW,tag = "half")
        elif tag == "close":
            self.canvas.create_image(0, 0, image=self.tachie_close, anchor=tk.NW,tag = "close")
        else:
            print("error:main.py,chenge_image,tag is unknown")

        #即反映
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
root.geometry('600x700')
window = w_talk(root)
root.mainloop()
