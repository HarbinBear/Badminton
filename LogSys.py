import tkinter as tk

import datetime

def print_with_time(message):
    current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f'[{current_time}] {message}')


def write_to_file( text , file_path='log.txt'):
    with open(file_path, 'a') as f:  # 打开文件，以'append'模式
        f.write( text )  # 写入字符串
        f.flush()  # 立即写入文件



# 利用write函数输出重定向，在app的init中绑定sys.stdout
class StreamToWidget(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        # 获取Text控件的内容总行数
        total_lines = int(self.widget.index('end-1c').split('.')[0])

        # 如果内容行数超过1000，删除超出的最早的一行
        if total_lines > 1000:
            self.widget.delete('1.0', '2.0')

        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        write_to_file( text )







