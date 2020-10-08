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
    displayMessage.pack()
    for fmt in formats:
        cb = tk.Checkbutton(text=fmt, onvalue=fmt)
        cb.pack()
#    format_list = tk.Listbox(height = len(formats), selectmode= 'extended')
#    format_list.pack()

window = tk.Tk()
urlEntry = tk.Entry(window,width = 50)
urlEntry.pack();
dlButton = tk.Button(window, text="Download", command=list_formats)
dlButton.pack()

window.mainloop()