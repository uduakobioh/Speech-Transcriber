import speech_recognition as sr
import os
from fpdf import FPDF
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


def listen():
    global transcript
    r = sr.Recognizer()
    r.pause_treshold = 0.8
    r.dynamic_energy_threshold = True
    m = sr.Microphone()

    with m as source:
        r.adjust_for_ambient_noise(m, 0.6)
        listen_message.configure(text='Listening...')
        audio = r.listen(source)
        listen_message.configure(text='Recognizing Audio')
        try:
            transcript = r.recognize_google(audio, show_all=False)
            listen_message.configure(text="Done Recognizing")
        except sr.UnknownValueError:
            pass
            listen_message.configure(text="System could not understand audio. Try Again")
        except sr.RequestError or sr.ConnectionAbortedError:
            listen_message.configure(text="Couldn't connect to google services. Check internet connection.")


def browse():
    path = filedialog.asksaveasfilename(initialdir="C:/Users/USER/Documents/",
                                        title="Select a File",
                                        filetypes=[('text files', '*.txt'), ('PDF', '.pdf'), ('all files', '*.*')],
                                        defaultextension=".txt",
                                        initialfile='transcript.txt')
    if path:
        save_location.delete(0, END)
        save_location.insert(0, path)


def save():
    filepath = save_location.get()
    name, extension = os.path.splitext(filepath)
    if extension == '.pdf':
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Times", size=14)
            pdf.write(5, transcript)
            pdf.output(filepath)
            output = f"Transcript saved to {filepath}"
        except:
            output = "Could not save speech"
    else:
        try:
            with open(filepath, 'w') as file:
                file.write(transcript)
            output = f"Transcript saved to {filepath}"
        except:
            output = "Could not save speech"
    save_message.configure(text=output)


window_bg = '#d2e59e'
root = Tk()
root.geometry('450x450')
root.title('SPEECH TRANSCRIBER')
root.configure(bg=window_bg)
root.resizable(False, False)

# creating the background image/text
img = ImageTk.PhotoImage(Image.open("background.png"))
background = Canvas(root,
                    width=450,
                    height=300,
                    bg=window_bg,
                    bd=0,
                    highlightthickness=0)
background.create_image(0, 0, anchor=NW, image=img)
background.create_text(220, 70, anchor=NW, text='to\nTEXT', font='Papyrus 50')
background.place(x=0, y=0)

# button to start listening for audio
listen_button = Button(root,
                       text='LISTEN',
                       bg='#235789',
                       font=('OCR-A BT', 35),
                       command=listen)
listen_button.place(x=134.8, y=300, width=179.5, height=60)
restart_icon = ImageTk.PhotoImage(Image.open("restart-icon.png"))
restart_button = Button(root,
                        image=restart_icon,
                        bg='#235789')
restart_button.place(x=321.5, y=307.5, width=45, height=45)
listen_message_frame = Frame(root,
                             bg=window_bg,
                             bd=0,
                             highlightthickness=0)
listen_message_frame.place(x=0, y=360, width=450, height=15)
listen_message = Label(listen_message_frame, bg=window_bg, font=('Arial', 10))
listen_message.pack()

# box to browse for file save location
save_location = Entry(root,
                      bg='white',
                      bd=2)
save_location.place(x=26, y=375, width=374, height=22.5)
folder = ImageTk.PhotoImage(Image.open("folder-icon.png"))
browse_button = Button(root,
                       bg='white',
                       bd=2,
                       image=folder,
                       command=browse)
browse_button.place(x=400, y=375, width=22.5, height=22.5)

# button to save transcript at specified location
save_button = Button(root,
                     text='SAVE',
                     bg='#235789',
                     font=('OCR-A BT', 25),
                     command=save)
save_button.place(x=164.5, y=402, width=120, height=30)
save_message_frame = Frame(root,
                           bg=window_bg,
                           bd=0,
                           highlightthickness=0)
save_message_frame.place(x=0, y=432, width=450, height=18)
save_message = Label(save_message_frame, bg=window_bg, font=('Arial', 10))
save_message.pack()

mainloop()
