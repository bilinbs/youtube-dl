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

window = tk.Tk()
window.title("YoutubeDL")

format_sel = ''
formats_checkbox_val = tk.StringVar()
fmtListBox = tk.Listbox()
url = ''

def formatChanged():
    global format_sel
    print(format_sel)
    print(formats_checkbox_val)

def progress_display(d):
    print(d['status'])
    print(repr(d))


def list_formats():
    global url
    url=[urlEntry.get()]
    fmtLog = FormatLogger()
    ytdl_opts = { 'listformats' : 'true' , 'logger': fmtLog}
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        format_list = ydl.download(url)
    global formats
    global formats_checkbox_val
    global fmtListBox
    formats = fmtLog.message.split('\n')
    displayText = formats.pop(0) + '\n' + formats.pop(0)
    displayMessage = tk.Label(text= displayText)
    displayMessage.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    #displayMessage.pack()
    rowNum = 0
    fmtListBox = tk.Listbox(height = len(formats), selectmode='extended')
    fmtListBox.grid(row = 2, column=0, sticky="ew")
    for fmt in formats:
        #cb = tk.Checkbutton(text=fmt, onvalue=fmt.split()[0], command=formatChanged, variable=formats_checkbox_val)
        #cb.grid(row=rowNum, column=0, sticky="w", padx=5, pady=5)
        fmtListBox.insert(rowNum, fmt)
        rowNum = rowNum + 1
#    format_list = tk.Listbox(height = len(formats), selectmode= 'extended')
#    format_list.pack()

def downloadSelection():
    global fmtListBox
    selected = fmtListBox.curselection()
    format_selected = ''
    if selected == ():
        format_selected = 'bestaudio/best'
    else:
        cur_select = []
        for sel in selected:
            cur_select.append(fmtListBox.get(sel).split()[0])
        format_selected = '+'.join(str(sel) for sel in cur_select)
    ydl_opts = {
        'format': format_selected,
        'progress_hooks': [progress_display]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        format_list = ydl.download(url)



#window.rowconfigure(0, minsize=640, weight=1)
#window.columnconfigure(0, minsize=480, weight=1)
#window.columnconfigure(1, minsize=80, weight=1)
urlEntry = tk.Entry(window,width = 50)
listButton = tk.Button(window, text="List Formats", command=list_formats)
dlButton = tk.Button(window, text="Download", command=downloadSelection)
urlEntry.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
listButton.grid(row=0, column=1, sticky="nw", padx=5)
dlButton.grid(row=0, column=2, sticky="nw", padx=5)
#urlEntry.pack()
#dlButton.pack()
window.mainloop()