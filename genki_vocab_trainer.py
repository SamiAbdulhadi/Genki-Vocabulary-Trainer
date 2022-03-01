"""Genki Vocab Trainer"""
import pandas as pd
import random
from playsound import playsound
from gtts import gTTS
import os
import tkinter as tk
import time
import threading

path = os.getcwd() + '\\'

running = True

#%% Tkinter App Construction
root = tk.Tk()
root.title('Genki Vocabulary Trainer')

AppCanvas = tk.Canvas(root, width = 400, height = 450, relief = 'raised')
AppCanvas.pack()

class label:
    def __init__(self, text, size, x, y):
        self.text = text
        self.size = size
        self.x = x
        self.y = y
    def create_label(self):
        lab = tk.Label(root, text = self.text)
        lab.config(font = ('helvetica', self.size))
        AppCanvas.create_window(self.x, self.y, window = lab)

label_title = label('Genki Vocabulary Trainer', 16, 200, 25).create_label()
label_description = label('Denote the selected vocab words with a "1" in vocab.xlsx', 10, 200, 70).create_label()
label_book = label('Book (1 or 2)', 14, 109, 140).create_label()
label_lesson = label('Lesson (1-12)', 14, 109, 180).create_label()
label_order = label('Prompt Order', 14, 109, 220).create_label()
label_repeat = label('Repeat', 14, 109, 260).create_label()
label_wait = label('Answer Time (sec)', 14, 109, 300).create_label()

entry_book = tk.Entry(root, width = 7)
entry_book.insert(0, '1')
entry_book.place(x=225, y=130)

entry_lesson = tk.Entry(root, width = 7)
entry_lesson.insert(0, '1')
entry_lesson.place(x=225, y=170)

order_v1 = tk.BooleanVar()
order_click = tk.Checkbutton(root, text = 'Japanese -> English', variable = order_v1, onvalue=True, offvalue=False, takefocus = 0).place(x = 220, y = 210)
order_v1.set(True)

repeat_v1 = tk.BooleanVar()
repeat_click = tk.Checkbutton(root, text = 'Repeat Once', variable = repeat_v1, onvalue=True, offvalue=False, takefocus = 0).place(x = 220, y = 250)
repeat_v1.set(False)

entry_wait = tk.Entry(root, width = 7)
entry_wait.insert(0, '3')
entry_wait.place(x=225, y=290)

#%% Vocab Functions
def vocab_speech(table, order, waittime, repeat):
    if running:
        play_index = random.randint(0, len(table)-1)
        file1 = f'{path}ja_speech.mp3'
        file2 = f'{path}eng_speech.mp3'
        
        if os.path.exists(f'{path}ja_speech.mp3'):
            os.remove(f'{path}ja_speech.mp3')
        if os.path.exists(f'{path}eng_speech.mp3'):
            os.remove(f'{path}eng_speech.mp3')
        
        ja_speech = gTTS(table.iloc[play_index, 1], lang='ja')
        ja_speech.save(file1)
        eng_speech = gTTS(table.iloc[play_index, 4])
        eng_speech.save(file2)
        
        if order == False:
            file1, file2 = file2, file1
        
        playsound(file1)
        time.sleep(waittime)
        playsound(file2)
        time.sleep(2)
        
        if repeat == True:
            playsound(file1)
            time.sleep(waittime)
            playsound(file2)
            time.sleep(2)

def Vocab_Looper():
    global running
    running = True
    book = entry_book.get()
    lesson = entry_lesson.get()
    order = order_v1.get()
    repeat = repeat_v1.get()
    wait = int(entry_wait.get())
    
    vocab_list = pd.read_excel(f'{path}vocab.xlsx', sheet_name=f'{book}-{lesson}')
    vocab_list = vocab_list.loc[vocab_list.Selected == 1].reset_index()
    
    repetition = 0    
    while repetition < 1000:
        vocab_speech(vocab_list, order, wait, repeat)
        repetition += 1
        
def start():        
    threading.Thread(target=Vocab_Looper).start()

def stop():
   global running
   running = False
      
play_button = tk.Button(root, text = 'Play', command = start, bg = 'dodgerblue', fg = 'white', font = ('helvetica', 12, 'bold'))
AppCanvas.create_window(170, 400, window = play_button)

pause_button = tk.Button(root, text = 'Stop', command = stop, bg = 'tomato', fg = 'white', font = ('helvetica', 12, 'bold'))
AppCanvas.create_window(230, 400, window = pause_button)

root.mainloop()