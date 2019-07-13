import tkinter as tk
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=5, column=5)
        self.create_widgets()

    def create_widgets(self):
        # 创建第一个容器用来存放标题
        fm_title = tk.Frame(width=400, height=50)
        tk.Label(fm_title, text='Please Input Keyword!', fg='red', width=50, height=3).grid(row=0, column=3)
        fm_title.grid()

        # 创建第二个容器用来放置参数设置区域
        fm_config = tk.Frame(self.master, width=200, height=100)
        # 首先需要一个keyword参数，包括label和entry
        lab_key = tk.Label(fm_config, text='Keyword:')
        lab_key.grid(row=0, column=0, sticky='W')
        ent_key = tk.Entry(fm_config, textvariable='Hello', width=15)
        ent_key.grid(row=0, column=1)

        lab_path = tk.Label(fm_config, text="Path:")
        lab_path.grid(row=1, column=0, sticky='W')
        var_path_str = tk.StringVar()
        var_path_str.set('c:\\zjg')
        ent_path = tk.Entry(fm_config, textvariable=var_path_str, width=15)
        ent_path.grid(row=1, column=1)
        fm_config.grid()

        # 创建第三个容器用来放置控制逻辑的按钮等
        fm_logic = tk.Frame(self.master, width=200, height=50)
        btn_getvalue = tk.Button(fm_logic, text='GetValue', width=15, bd=3,
                                 command=lambda: self.get_keyword(ent_key.get()))
        btn_getvalue.grid(row=0, column=0)
        tk.Button(fm_logic, text='Quit', command=self.master.quit).grid(row=0, column=1, padx=10, pady=4)
        fm_logic.grid()

    @staticmethod
    def get_keyword(keyword):
        messagebox.showinfo('Info', keyword)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x200')  # 设置窗口大小
    app = Application(master=root)
    app.mainloop()
