import Tkinter as tk

class Window(tk.Frame):
    def __init__(self, master=None, view=None):
        tk.Frame.__init__(self, master)
        self.gui_view = view
        self.init_window()
        self.master = master
        self.init_window()

    def init_window(self):
        test_slider = Scale(self.master, from_=0, to=100)
        #test_slider.pack()
        pass

class View():
    def __init__(self):
        self.root = tk.Tk()
        self.gui_window = Window(master=None, view=self)
        self.gui_window.pack()
        self.refresh()
        self.root.mainloop()

    def refresh(self):
        self.root.update()