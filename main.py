import tkinter as tk
from tkinter import ttk
import getindex
# from tkinter import messagebox
import time


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.label_info = None
        self.create_widgets()

    def create_widgets(self):
        # 使用place的布局方式来设定
        C = tk.Canvas(self.master, height=400, width=500)
        C.pack()
        # 填充标题
        top_frame = tk.Frame(self.master)
        top_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.05, anchor='n')
        title_lab = tk.Label(top_frame, font=50, text='Please Input Keyword')
        title_lab.place(relwidth=0.75, relheight=0.8, relx=0.1, rely=0.05)
        # 内容区域
        content_frame = tk.Frame(self.master, bg='#42c2f4', bd=3)
        content_frame.place(relx=0.5, rely=0.15, relwidth=0.85, relheight=0.68, anchor='n')
        lab_key = tk.Label(content_frame, text='KeyWord:', bg='#42c2f4')
        lab_key.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)
        ent_key = tk.Entry(content_frame)
        ent_key.place(relx=0.35, rely=0.1, relwidth=0.51, relheight=0.1)
        lab_path = tk.Label(content_frame, text='SavePath:', bg='#42c2f4')
        lab_path.place(relx=0.1, rely=0.25, relwidth=0.2, relheight=0.1)
        var_path_str = tk.StringVar()
        var_path_str.set('c:\\zjg')
        ent_path = tk.Entry(content_frame, textvariable=var_path_str)
        ent_path.place(relx=0.35, rely=0.25, relwidth=0.51, relheight=0.1)
        # 创建开始时间和结束时间输入栏
        startdate_lab = tk.Label(content_frame, text='开始时间')
        startdate_lab.place(relx=0.1, rely=0.4, relwidth=0.15, relheight=0.1)
        startdate_ent = tk.Entry(content_frame)
        startdate_ent.place(relx=0.265, rely=0.4, relwidth=0.2, relheight=0.1)
        enddate_lab = tk.Label(content_frame, text='结束时间')
        enddate_lab.place(relx=0.5, rely=0.4, relwidth=0.15, relheight=0.1)
        enddate_ent = tk.Entry(content_frame)
        enddate_ent.place(relx=0.665, rely=0.4, relwidth=0.2, relheight=0.1)
        # 创建选择栏，用于选择爬取目标
        comb_lab = tk.Label(content_frame, text='爬取目标:')
        comb_lab.place(relx=0.1, rely=0.6, relwidth=0.18, relheight=0.1)
        comb = ttk.Combobox(content_frame, state='readonly', width=5)
        comb['value'] = ['搜索指数', '资讯指数', '媒体指数']
        comb.place(relx=0.3, rely=0.6, relwidth=0.2, relheight=0.1)
        comb.current(0)
        # Info Area
        self.label_info = tk.Label(content_frame)
        self.label_info.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.2)
        # 按钮区域
        btn_frame = tk.Frame(self.master, bd=5)
        btn_frame.place(relx=0.5, rely=0.96, relwidth=0.75, relheight=0.1, anchor='s')
        btn_getvalue = tk.Button(btn_frame, text='GetValue'
                                 , command=lambda: self.get_params(ent_key.get(),
                                                                   startdate_ent.get(),
                                                                   enddate_ent.get(),
                                                                   comb.get(),
                                                                   ent_path.get()))
        btn_getvalue.place(relx=0.25, rely=1, relwidth=0.2, relheight=1, anchor='s')
        # 退出按钮
        btn_quit = tk.Button(btn_frame, text='Quit', command=self.master.quit)
        btn_quit.place(relx=0.5, rely=1, relwidth=0.2, relheight=1, anchor='s')

    def get_params(self, keyword, startdate, enddate, target, path):
        # 这里要引用百度指数数据获取逻辑
        self.label_info['text'] = 'Get keyworld: {}'.format(keyword)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    app = Application(master=root)
    app.mainloop()
