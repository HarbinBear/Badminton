import sys
import threading
import tkinter as tk
from tkinter import Canvas, PhotoImage  # 导入Canvas和PhotoImage
from PIL import Image, ImageTk
import json
from Badminton import load_config, order_it , book , print_order_status
from LogSys import StreamToWidget , print_with_time
from datetime import datetime, timedelta
from Model import Model

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.model = Model()
        self.model.initParams()
        self.model.load_from_json('config.json')
        self.create_widgets()
        sys.stdout = StreamToWidget(self.status_text)


    def create_widgets(self):
        # 创建一个Label或Canvas
        background_label = tk.Label(root)
        background_label.place(anchor="center", relx=0.5, rely=0.55)

        # # 将图片设置为其背景
        # # 打开图像
        # img = Image.open('multi.png')
        # img = img.convert("RGBA")
        #
        # # 获取alpha通道
        # alpha = img.split()[3]
        #
        # # 创建一个新的alpha通道，将其值设置为原始alpha通道的20%
        # alpha = alpha.point(lambda p: p * 0.2)
        #
        # # 使用新的alpha通道替换原始图像
        # img.putalpha(alpha)
        #
        # # 保存新图像
        # img.save('multi_trans.png')

        background_image = tk.PhotoImage(file='multi_trans.png')

        background_label.image = background_image  # keep a reference!
        background_label.configure(image=background_image)

        # 将背景Label或Canvas移到底层
        # background_label.lift()

        row_num = 0

        space_label = tk.Label(root ).grid(row=row_num, column=0 , padx=10 , pady=20 )

        row_num += 1

        # 用户信息选择
        self.config = load_config()
        self.user_options = [user["OpenId"] for user in self.config["USERS_INFO"]]

        tk.Label(root, text="User:", bg="light blue").grid(row=row_num, column=0 , padx=10 , pady=10 )  # 设置背景色
        self.user_var = tk.StringVar(root)
        self.user_var.set(self.user_options[0])  # 默认选项
        self.user_menu = tk.OptionMenu(root, self.user_var, *self.user_options, command=self.user_select)
        self.user_menu.grid( row = row_num , column=1  , padx=10 , pady=10 , sticky=tk.W )

        row_num += 1

        tk.Label(root,text="Token:", bg="light blue").grid(row=row_num, column=0 , padx=10 , pady=10 )  # 设置背景色
        self.token_entry = tk.Entry(root , width=130  , fg= "blue"  )
        self.token_entry.grid( row = row_num , column=1  , padx=10 , pady=10, sticky=tk.W )

        # 初始token
        self.user_select()

        time_options = ["{}:00~{}:00".format(i, i + 1) for i in range(15, 21)]
        time_options.append("无")

        row_num += 1

        # 时间选项
        tk.Label(root,text="第一场:", bg="light blue").grid(row=row_num, column=0 , padx=10 , pady=10 )  # 设置背景色
        self.time_var1 = tk.StringVar(root)
        self.time_var1.set(time_options[self.model.begin_time1 - 15 ])  # 默认选项
        self.time_menu1 = tk.OptionMenu(root, self.time_var1, *time_options , command= self.update_time1 )
        self.time_menu1.grid( row = row_num , column=1  , padx=10 , pady=10, sticky=tk.W )

        row_num += 1


        tk.Label(root,text="第二场:", bg="light blue").grid(row=row_num, column=0 , padx=10 , pady=10 )
        self.time_var2 = tk.StringVar(root)
        self.time_var2.set(time_options[ self.model.begin_time2 - 15 ])  # 默认选项
        self.time_menu2 = tk.OptionMenu(root, self.time_var2, *time_options ,  command= self.update_time2 )
        self.time_menu2.grid( row = row_num , column=1  , padx=10 , pady=10 , sticky=tk.W)


        row_num += 1

        day_options = ["第一天","第二天"]

        tk.Label(root, text="第几天呢", bg="light blue").grid(row=row_num, column=0, padx=10, pady=10)
        self.day_var = tk.StringVar(root)
        self.day_var.set(day_options[ self.model.add_Day ])  # 默认选项
        self.day_menu = tk.OptionMenu(root, self.day_var, *day_options, command= self.update_day)
        self.day_menu.grid(row=row_num, column=1, padx=10, pady=10, sticky=tk.W)

        row_num += 1

        weekday_options = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        order_date = (datetime.now() + timedelta(days=2)).date()  # 后天日期
        order_weekday = order_date.weekday()

        tk.Label(root, text="约周几咧", bg="light blue").grid(row=row_num, column=0, padx=10, pady=10)
        self.order_week_strvar = tk.StringVar(root)
        self.order_week_strvar.set(weekday_options[ order_weekday ])  # 默认选项
        self.order_week_menu = tk.OptionMenu(root, self.order_week_strvar, *weekday_options, command= self.update_order_week)
        self.order_week_menu.grid(row=row_num, column=1, padx=10, pady=10, sticky=tk.W)

        row_num += 1


        # 开始预约按钮
        self.go_button = tk.Button(root, text="开始预约", command=self.start_booking)
        self.go_button.grid( row = row_num , column=1   , padx=10 , pady=10 )


        row_num += 1

        # 立即预约
        tk.Label(root, text="立即预约", bg="light blue").grid(row=row_num, column=0, padx=10, pady=10)
        self.model.debug_var = tk.BooleanVar()
        self.debug_checkbox = tk.Checkbutton(root, variable=self.model.debug_var )
        self.debug_checkbox.grid(row=row_num, column=1, padx=10, pady=10, sticky=tk.W)
        row_num += 1

        space_label3 = tk.Label(root ).grid( row=row_num, column=0 , padx=10 , pady=10 )

        row_num += 1



        # 日志
        self.status_text = tk.Text(root , height= 10, width= 130 , bg="light yellow"  )
        self.status_text.grid( row = row_num  ,column=1 , padx=10 , pady=20  )


    # 选择学号时，清空token
    def user_select(self, *args ):
        selected_user = [user for user in self.config["USERS_INFO"] if user["OpenId"] == self.user_var.get()][0]
        # self.token_entry.delete(0, tk.END)  # 清除原有内容
        # self.token_entry.insert(0, selected_user["JWTUserToken"])  # 填充新的token
        # self.model.token = selected_user["JWTUserToken"]
        self.model.openid = selected_user["OpenId"]
        self.model.name = selected_user["name"]
        print_order_status()

    def update_day(self , *args ):
        self.model.add_Day = 0 if self.day_var.get() == "第一天" else 1
        print_order_status()

    def update_order_week(self , *args ):
        self.model.order_weekday_str = self.order_week_strvar.get()
        print_order_status()

    # # 更新token
    # def update_token(self , *args):
    #     self.model.token = self.token_entry.get()
    #     print_order_status()

    def update_time1(self , *args):
        time_str1 = self.time_var1.get()
        if time_str1 != "无" :
            self.model.begin_time1 = int(time_str1.split(":")[0])  # 提取出小时部分，并转换为整数类型
            self.model.time1_needed = True
        else :
            self.model.time1_needed = False
        self.calc_sum()
        print_order_status()


    def update_time2(self , *args):
        time_str2 = self.time_var2.get()
        if time_str2 != "无" :
            self.model.begin_time2 = int(time_str2.split(":")[0])  # 提取出小时部分，并转换为整数类型
            self.model.time2_needed = True
        else :
            self.model.time2_needed = False
        self.calc_sum()
        print_order_status()

    def start_booking(self , *args):
        # token无法响应式更新，只使用开始按钮进行单独更新
        self.model.token = self.token_entry.get()
        print_order_status()

        if self.model.started == True :
            return

        print_with_time("start")
        self.model.started = True

        threading.Thread(target=self.start_booking_thread, daemon=True ).start()


    def start_booking_thread(self):
        book( )


    def calc_sum(self):
        sum = 0
        if self.time_var1.get() != "无" :
            sum += 1
        if self.time_var2.get() != "无" :
            sum += 1
        self.model.sum = sum

root = tk.Tk()
root.geometry("1024x800")
root.title("CUC羽毛球小助手 v0.5")
# root.attributes("-alpha", 0.9)
app = Application(master=root)
app.mainloop()

