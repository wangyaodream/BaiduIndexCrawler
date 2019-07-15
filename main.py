import tkinter as tk
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # # 创建第一个容器用来存放标题
        # fm_title = tk.Frame(width=400, height=50)
        # tk.Label(fm_title, text='Please Input Keyword!', fg='red', width=50, height=3).grid(row=0, column=3)
        # fm_title.grid()
        #
        # # 创建第二个容器用来放置参数设置区域
        # fm_config = tk.Frame(self.master, width=200, height=100)
        # # 首先需要一个keyword参数，包括label和entry
        # lab_key = tk.Label(fm_config, text='Keyword:')
        # lab_key.grid(row=0, column=0, sticky='W')
        # ent_key = tk.Entry(fm_config, textvariable='Hello', width=15)
        # ent_key.grid(row=0, column=1)
        #
        # lab_path = tk.Label(fm_config, text="Path:")
        # lab_path.grid(row=1, column=0, sticky='W')
        # var_path_str = tk.StringVar()
        # var_path_str.set('c:\\zjg')
        # ent_path = tk.Entry(fm_config, textvariable=var_path_str, width=15)
        # ent_path.grid(row=1, column=1)
        # fm_config.grid()
        #
        # # 创建第三个容器用来放置控制逻辑的按钮等
        # fm_logic = tk.Frame(self.master, width=200, height=50)
        # btn_getvalue = tk.Button(fm_logic, text='GetValue', width=15, bd=3,
        #                          command=lambda: self.get_keyword(ent_key.get()))
        # btn_getvalue.grid(row=0, column=0)
        # tk.Button(fm_logic, text='Quit', command=self.master.quit).grid(row=0, column=1, padx=10, pady=4)
        # fm_logic.grid()

        # 使用place的布局方式来设定
        C = tk.Canvas(self.master, height=400, width=500)
        C.pack()
        # 填充标题
        top_frame = tk.Frame(self.master)
        top_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')
        title_lab = tk.Label(top_frame, font=50, text='Please Input Keyword')
        title_lab.place(relwidth=0.75, relheight=0.8, relx=0.1, rely=0.1)
        # 内容区域
        content_frame = tk.Frame(self.master, bg='#42c2f4', bd=3)
        content_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.6, anchor='n')
        lab_key = tk.Label(content_frame, text='KeyWord:', bg='#42c2f4')
        lab_key.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)
        ent_key = tk.Entry(content_frame)
        ent_key.place(relx=0.35, rely=0.1, relwidth=0.4, relheight=0.1)
        lab_path = tk.Label(content_frame, text='Path:', bg='#42c2f4')
        lab_path.place(relx=0.1, rely=0.25, relwidth=0.2, relheight=0.1)
        var_path_str = tk.StringVar()
        var_path_str.set('c:\\zjg')
        ent_path = tk.Entry(content_frame, textvariable=var_path_str)
        ent_path.place(relx=0.35, rely=0.25, relwidth=0.4, relheight=0.1)
        # Info Area
        label_info = tk.Label(content_frame)
        label_info.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.5)
        # 按钮区域

    @staticmethod
    def get_keyword(keyword):
        # 这里要引用百度指数数据获取逻辑
        messagebox.showinfo('Info', keyword)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    app = Application(master=root)
    app.mainloop()
