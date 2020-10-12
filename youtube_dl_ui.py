from __future__ import unicode_literals
import youtube_dl
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

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
fmtListBox_vid = tk.Listbox()
fmtListBox_aud = tk.Listbox()
fmtListBox_av = tk.Listbox()
url = ''
dlProgressBar = ttk.Progressbar()
dlLabel = tk.Label()

def progress_display(d):
    global dlProgressBar
    global window
    #print(d['status'])
    #print(repr(d))
    if d['status'] == 'downloading':
        precentValue = d['_percent_str'].strip('%')
        print("ivide" + precentValue)
        dlProgressBar['value'] = precentValue
        dlLabel['text'] = 'Downloading selected formats: ' + format_selected + ' @' + d['_speed_str'] + ' ETA:'+ d['_eta_str']
        window.update()
    elif d['status'] == 'finished':
        messagebox.showinfo('Dowload Complete', 'Downloaded ' + d['_total_bytes_str'] + ' to \n' + d['filename'])
        dlLabel['text'] = 'Completed downloading ' +  d['_total_bytes_str']

def getSelectionListBox(listbox, formats, rowNum):
    listbox.destroy()
    listbox = tk.Listbox(height = len(formats), selectmode='browse', exportselection=0)
    listbox.grid(row = rowNum, column=0, columnspan = 3, sticky="ew")
    return listbox

def insertToListBox(formats, listbox):
    rowNum = 0
    for fmt in formats:
        listbox.insert(rowNum, fmt)
        rowNum = rowNum + 1

def list_formats():
    global url
    global formats
    global formats_checkbox_val
    global fmtListBox
    global dlButton
    global fmtListBox_vid
    global fmtListBox_aud
    global fmtListBox_av
    url=[urlEntry.get().strip()]
    fmtLog = FormatLogger()
    ytdl_opts = { 'listformats' : 'true' , 'logger': fmtLog}
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        format_list = ydl.download(url)
    formats = fmtLog.message.split('\n')
    displayText = 'If no formats from below are selected, the best available will be downlaoded \n' + formats.pop(0) + '\n' + '\t'.join(formats.pop(0).split())
    displayMessage = tk.Label(text= displayText, justify='left')
    displayMessage.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    videoOnlyFormats = list(filter(lambda x: 'video only' in x, formats))
    audioOnlyFormats = list(filter(lambda x: 'audio only' in x, formats))
    avFormats = list(filter(lambda x: not ('audio only' in x or 'video only' in x), formats))
    label_vid = tk.Label(text='Video only formats: (select one)')
    label_vid.grid(row = 2, column=0, columnspan = 3, sticky="ew")
    fmtListBox_vid = getSelectionListBox(fmtListBox_vid, videoOnlyFormats, 3)
    label_aud = tk.Label(text='Audio only formats: (select one)')
    label_aud.grid(row = 4, column=0, columnspan = 3, sticky="ew")
    fmtListBox_aud = getSelectionListBox(fmtListBox_aud, audioOnlyFormats, 5)
    label_av = tk.Label(text='Audio&Video formats: If one of the below formats are selected, choices made above will be ignored')
    label_av.grid(row = 6, column=0, columnspan = 3, sticky="ew")
    fmtListBox_av = getSelectionListBox(fmtListBox_av, avFormats,7)
    insertToListBox(videoOnlyFormats, fmtListBox_vid)
    insertToListBox(audioOnlyFormats, fmtListBox_aud)
    insertToListBox(avFormats, fmtListBox_av) 
    dlButton.config(state='normal')

def downloadSelection():
    global rowNumWin
    global window
    global dlProgressBar
    global dlLabel
    global format_selected
    global url
    global fmtListBox_vid
    global fmtListBox_aud
    global fmtListBox_av
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
            print(selectedVideo)
        if selectedAudio != ():
            if format_selected != '':
                format_selected = format_selected + '+'
            format_selected = format_selected + fmtListBox_aud.get(selectedAudio).split()[0]
            
    separator = ttk.Separator(window)
    separator.grid(row = 8, column=0, columnspan = 4, sticky="ew")    
    dlProgressBar = ttk.Progressbar(window, orient='horizontal', mode='determinate', maximum='100', value='0')
    dlProgressBar.grid(row = 9, column = 1, columnspan = 2, sticky="ew")    
    dlLabel = tk.Label(window, text='Downloading selected formats: ' + format_selected)
    dlLabel.grid(row = 9, column = 0, sticky="ew")
    ydl_opts = {
        'format': format_selected,
        'progress_hooks': [progress_display]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        format_list = ydl.download(url)
    
label_dl = tk.Label(window, text = 'Enter the video url:')
urlEntry = tk.Entry(window,width = 50)
listButton = tk.Button(window, text="List Formats", command=list_formats)
dlButton = tk.Button(window, text="Download", command=downloadSelection, state='disabled')
label_dl.grid(row = 0, column=0, sticky = "nw", padx=5)
urlEntry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
listButton.grid(row=0, column=2, sticky="nw", padx=5)
dlButton.grid(row=0, column=3, sticky="nw", padx=5)
window.mainloop()
