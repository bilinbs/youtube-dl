from __future__ import unicode_literals
import youtube_dl
import tkinter as tk

class FormatLogger(object):
    message = ''
    def debug(self, msg):
        self.message =self. message + msg
    def warning(self, msg):
        print('Warning'+ msg)
    def error(self, msg):
        print('Error'+ msg)
    def info(self, msg):
        print('Info'+msg) 

def list_formats():
    url=[urlEntry.get()]
    fmtLog = FormatLogger()
    ytdl_opts = { 'listformats' : 'true' , 'logger': fmtLog}
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        format_list = ydl.download(url)
    formats = fmtLog.message.split('\n')
    displayText = formats.pop(0) + '\n' + formats.pop(0)
    displayMessage = tk.Label(text= displayText)
    displayMessage.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    #displayMessage.pack()
    rowNum = 2
    for fmt in formats:
        cb = tk.Checkbutton(text=fmt, onvalue=fmt)
        cb.grid(row=rowNum, column=0, sticky="w", padx=5, pady=5)
        rowNum = rowNum + 1
#    format_list = tk.Listbox(height = len(formats), selectmode= 'extended')
#    format_list.pack()

window = tk.Tk()
window.title("YoutubeDL")
#window.rowconfigure(0, minsize=640, weight=1)
#window.columnconfigure(1, minsize=480, weight=1)
urlEntry = tk.Entry(window,width = 50)
dlButton = tk.Button(window, text="Download", command=list_formats)
urlEntry.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
dlButton.grid(row=0, column=1, sticky="nw", padx=5)
#urlEntry.pack()
#dlButton.pack()
window.mainloop()