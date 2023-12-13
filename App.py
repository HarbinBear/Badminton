import sys
import threading
import tkinter as tk
import json
from Badminton import load_config, order_it , book
from datetime import datetime, timedelta


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        sys.stdout = StreamToWidget(self.status_text)


    def create_widgets(self):
        # 用户信息选择
        self.config = load_config()
        self.user_options = [user["OpenId"] for user in self.config["USERS_INFO"]]

        tk.Label(root,text="User:").pack()
        self.user_var = tk.StringVar(root)
        self.user_var.set(self.user_options[0])  # 默认选项
        self.user_menu = tk.OptionMenu(root, self.user_var, *self.user_options, command=self.user_select)
        self.user_menu.pack(pady=10)

        tk.Label(root,text="Token:").pack()
        self.token_entry = tk.Entry(root)
        self.token_entry.pack(pady=10)

        # 初始token
        self.update_token()

        # 时间选项
        tk.Label(root,text="第一场:").pack()
        time_options = ["{}:00~{}:00".format(i, i + 1) for i in range(15, 21)]
        self.time_var1 = tk.StringVar(root)
        self.time_var1.set(time_options[0])  # 默认选项
        self.time_menu1 = tk.OptionMenu(root, self.time_var1, *time_options)
        self.time_menu1.pack(pady=10)

        tk.Label(root,text="第二场:").pack()
        self.time_var2 = tk.StringVar(root)
        self.time_var2.set(time_options[0])  # 默认选项
        self.time_menu2 = tk.OptionMenu(root, self.time_var2, *time_options)
        self.time_menu2.pack(pady=10)

        # 开始预约按钮
        self.go_button = tk.Button(root, text="开始预约", command=self.start_booking)
        self.go_button.pack(pady=10)

        # 状态栏
        # self.status_var = tk.StringVar(root, value="等待预约")
        # self.status_label = tk.Label(root, textvariable=self.status_var)
        # self.status_label.pack()
        tk.Label(root,text="日志:").pack()
        self.status_text = tk.Text(root)
        self.status_text.pack(pady=10)

    def user_select(self, value):
        self.update_token()

    def update_token(self):
        selected_user = [user for user in self.config["USERS_INFO"] if user["OpenId"] == self.user_var.get()][0]
        self.token_entry.delete(0, tk.END)  # 清除原有内容
        self.token_entry.insert(0, selected_user["JWTUserToken"])  # 填充新的token

    def start_booking(self):
        print("start")
        threading.Thread(target=self.start_booking_thread, daemon=True ).start()


    def start_booking_thread(self):
        openid = self.user_var.get()
        token = self.token_entry.get()

        time_str1 = self.time_var1.get()
        hour1 = int(time_str1.split(":")[0])  # 提取出小时部分，并转换为整数类型

        time_str2 = self.time_var2.get()
        hour2 = int(time_str2.split(":")[0])  # 提取出小时部分，并转换为整数类型

        book( openid , token , hour1 , hour2 )


    def log_message(self, message):
        # 更新状态文本框
        self.status_text.insert(tk.END, message + '\n')
        # 自动滚动到底部
        self.status_text.see(tk.END)
        # 更新界面
        self.status_text.update()



class StreamToWidget(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)




root = tk.Tk()
root.geometry("800x600")
root.title("Badminton v0.1")
app = Application(master=root)
app.mainloop()

