import tkinter as tk
from app.gui.app_window import Application

#Create window
window = tk.Tk()
window.geometry("1200x800")

app = Application(master=window)

app.mainloop()




