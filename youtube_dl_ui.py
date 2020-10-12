from __future__ import unicode_literals
import youtube_dl
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox 

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
fmtListBox_vid = tk.Listbox()
fmtListBox_aud = tk.Listbox()
fmtListBox_av = tk.Listbox()
url = ''
dlProgressBar = ttk.Progressbar()
rowNumWin = 0

def formatChanged():
    global format_sel
    print(format_sel)
    print(formats_checkbox_val)

def progress_display(d):
    global dlProgressBar
    global window
    #print(d['status'])
    #print(repr(d))
    if d['status'] == 'downloading':
        precentValue = d['_percent_str'].strip('%')
        print("ivide" + precentValue)
        dlProgressBar['value'] = precentValue
        window.update()
    elif d['status'] == 'downloaded':
        messagebox.showinfo('Dowload Complete', repr(d))

def list_formats():
    global url
    url=[urlEntry.get().strip()]
    fmtLog = FormatLogger()
    ytdl_opts = { 'listformats' : 'true' , 'logger': fmtLog}
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        format_list = ydl.download(url)
    global formats
    global formats_checkbox_val
    global fmtListBox
    global dlButton
    formats = fmtLog.message.split('\n')
    displayText = 'If no formats from below are selected, the best available will be downlaoded \n' + formats.pop(0) + '\n' + '\t'.join(formats.pop(0).split())
    displayMessage = tk.Label(text= displayText, justify='left')
    displayMessage.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    videoOnlyFormats = list(filter(lambda x: 'video only' in x, formats))
    audioOnlyFormats = list(filter(lambda x: 'audio only' in x, formats))
    avFormats = list(filter(lambda x: not ('audio only' in x or 'video only' in x), formats))
    label_vid = tk.Label(text='Video only formats: (select one)')
    label_vid.grid(row = 2, column=0, columnspan = 3, sticky="ew")
    fmtListBox_vid = tk.Listbox(height = len(videoOnlyFormats), selectmode='browse')
    fmtListBox_vid.grid(row = 3, column=0, columnspan = 3, sticky="ew")
    label_aud = tk.Label(text='Audio only formats: (select one)')
    label_aud.grid(row = 4, column=0, columnspan = 3, sticky="ew")
    fmtListBox_aud = tk.Listbox(height = len(audioOnlyFormats), selectmode='browse')
    fmtListBox_aud.grid(row = 5, column=0, columnspan = 3, sticky="ew")
    label_av = tk.Label(text='Audio&Video formats: If one of the below formats are selected, choices made above will be ignored')
    label_av.grid(row = 6, column=0, columnspan = 3, sticky="ew")
    fmtListBox_av = tk.Listbox(height = len(audioOnlyFormats), selectmode='browse')
    fmtListBox_av.grid(row = 7, column=0, columnspan = 3, sticky="ew")
    rowNum = 0
    for fmt in videoOnlyFormats:
        fmtListBox_vid.insert(rowNum, fmt)
        rowNum = rowNum + 1
    rowNum = 0    
    for fmt in audioOnlyFormats:
        fmtListBox_aud.insert(rowNum, fmt)
        rowNum = rowNum + 1
    rowNum = 0    
    for fmt in avFormats:
        fmtListBox_av.insert(rowNum, fmt)
        rowNum = rowNum + 1    
    dlButton.config(state='normal')

def downloadSelection():
    global fmtListBox
    global rowNumWin
    global window
    global dlProgressBar
    selectedVideo = fmtListBox_vid.curselection()
    selectedAudio = fmtListBox_aud.curselection()
    selectedAV = fmtListBox_av.curselection()
    format_selected = ''
    if selectedAV == () and selectedVideo == () and selectedAudio == ():
        format_selected = 'bestaudio/best'
    elif selectedAV != ():
        format_selected = fmtListBox_av.get(selectedAV).split()[0]
    else:
        format_selected = ''
        if selectedVideo != ():
            format_selected = fmtListBox_vid.get(selectedVideo).split()[0]
        if selectedAudio != ():
            if format_selected != '':
                format_selected = format_selected + '+'
            format_selected = format_selected + selectedAudio.get(selectedAudio).split()[0]
            
        #cur_select = []
        #for sel in selected:
        #    cur_select.append(fmtListBox.get(sel).split()[0])
        #format_selected = '+'.join(str(sel) for sel in cur_select)
    dlProgressBar = ttk.Progressbar(window, orient='horizontal', mode='determinate', maximum='100', value='0')
    dlProgressBar.grid(row = 8, column = 1, columnspan = 2, sticky="ew")    
    ydl_opts = {
        'format': format_selected,
        'progress_hooks': [progress_display]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        format_list = ydl.download(url)
    
    


#window.rowconfigure(0, minsize=640, weight=1)
#window.columnconfigure(0, minsize=480, weight=1)
#window.columnconfigure(1, minsize=80, weight=1)
label_dl = tk.Label(window, text = 'Enter the video url:')
urlEntry = tk.Entry(window,width = 50)
listButton = tk.Button(window, text="List Formats", command=list_formats)
dlButton = tk.Button(window, text="Download", command=downloadSelection, state='disabled')
label_dl.grid(row = 0, column=0, sticky = "nw", padx=5)
urlEntry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
listButton.grid(row=0, column=2, sticky="nw", padx=5)
dlButton.grid(row=0, column=3, sticky="nw", padx=5)
#urlEntry.pack()
#dlButton.pack()
window.mainloop()
