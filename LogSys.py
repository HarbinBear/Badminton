import tkinter as tk

import datetime

def print_with_time(message):
    current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f'[{current_time}] {message}')



class StreamToWidget(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        # self.widget.config(text=text)






