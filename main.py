import tkinter as tk
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 创建第一个容器用来存放标题
        fm_title = tk.Frame(self.master)
        tk.Label(fm_title, text='Please Input Keyword!', fg='red').pack(side='top')
        fm_title.pack()

        # 创建第二个容器用来放置参数设置区域
        fm_config = tk.Frame(self.master)
        # 首先需要一个keyword参数，包括label和entry
        lab_key = tk.Label(fm_config, text='Keyword:')
        lab_key.pack(side='left')
        ent_key = tk.Entry(fm_config, text="", width=15)
        ent_key.pack(side='right')
        lab_path = tk.Label(fm_config, text="Path:")
        lab_path.pack(side='left')
        fm_config.pack()

        # 创建第三个容器用来放置控制逻辑的按钮等
        fm_logic = tk.Frame(self.master)
        btn_getvalue = tk.Button(fm_logic, text='GetValue', width=15, bd=3,
                                 command=lambda: self.get_keyword(ent_key.get()))
        btn_getvalue.pack(side='left')
        tk.Button(fm_logic, text='Quit', command=self.master.quit).pack(side='right')
        fm_logic.pack()

    @staticmethod
    def get_keyword(keyword):
        messagebox.showinfo('Info', keyword)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x200')
    app = Application(master=root)
    app.mainloop()