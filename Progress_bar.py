import tkinter as tk
from tkinter import ttk
import threading
import time

def process_event():
    for i in range(101):
        time.sleep(0.1)
        progress['value'] = i
        root.update_idletasks()

def start_thread():
    t = threading.Thread(target=process_event)
    t.start()

root = tk.Tk()
root.title("Progress Bar Example")

progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress.pack(pady=20)

start_button = ttk.Button(root, text="Start", command=start_thread)
start_button.pack(pady=10)

root.mainloop()