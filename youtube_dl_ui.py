from __future__ import unicode_literals
import youtube_dl

import tkinter as tk
window = tk.Tk()
urlEntry = tk.Entry()
urlEntry.pack();
dlButton = tk.Button(text="Download")
dlButton.pack()

url=[urlEntry.get()]

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

fmtLog = FormatLogger()
ytdl_opts = { 'listformats' : 'true' , 'logger': fmtLog}
with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
    format_list = ydl.download(url)

formats = fmtLog.message.split('\n')
displayText = formats.pop(0) + '\n' + formats.pop(0)

for fmt in formats:
    cb = tk.Checkbutton(text=fmt, onvalue=fmt)
    cb.pack()