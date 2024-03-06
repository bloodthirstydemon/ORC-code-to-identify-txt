# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:35:44 2024

@author: mitul_akbari
"""

import cv2
import tkinter as tk
from PIL import Image, ImageTk
import pytesseract
import time 


# =============================================================================
# specify the path of binary file for tesseract
# =============================================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =============================================================================
# class for camera application
# =============================================================================

class CameraApp:
    
    #initialise attributes to the class
    
    def __init__(self, window, window_title, video_source):
        
        # main window
        self.window = window
        self.window.title(window_title)
        
        #select video sourse and resolution
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        #self.cap = ueye.HIDS(0)
        #self.change_res(720, 720)                              ####we can select resolution of camera
        
        #add video feed window to canvas
        self.canvas = tk.Canvas(window)
        self.canvas.pack(side=tk.LEFT, padx=10)  
        
        #toggle button to start Acquisition and save data
        self.toggle_btn = tk.Button(text="Acquisition", width=12, relief="raised", command=self.Start_btn)
        self.toggle_btn.pack(pady=5)
        
        #text box for referance
        self.text_widget = tk.Text(window, wrap=tk.WORD, height=50, width=80)
        self.text_widget.pack(side=tk.RIGHT, padx=10)
        
        #quit button for main window
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(pady=10)
        
        #create a text file to store the data
        self.CAATF()
        
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = self.convert_frame_to_image(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Call read_frame to update the text widget
            if self.toggle_btn.config('relief')[-1] == 'sunken':
                self.read_frame(frame)
                self.update_time()
            else:
                pass
            
        self.window.after(1000, self.update)                  # Waiting time is in ms also defines capture(frame) rate
    
    
    def change_res(self, width, height):
        self.cap.set(3, width)
        self.cap.set(4, height)
         
    def Start_btn(self):

        if self.toggle_btn.config('relief')[-1] == 'sunken':
            self.toggle_btn.config(relief="raised")
        else:
            self.toggle_btn.config(relief="sunken")
            
            
    def CAATF(self):                                            #creat and append to file
        self.file = open("data.txt", "a")
        
        
    def convert_frame_to_image(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo
    
        
    def read_frame(self, frame):
        
# =============================================================================
#         immportant to read the documentation for pytesseract here to identify text accurately
#         By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
#         we need to convert from BGR to RGB format/mode:
# =============================================================================

        cv2.imwrite('photo.png', frame)
        photo = cv2.imread(r'photo.png')
        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(photo)
        self.file.write(f'{text}'+', ')
        self.text_widget.insert(tk.END, f'{text}'+', ')  
        
    
    def update_time(self):
        seconds = time.time()
        times = time.ctime(seconds)
        self.file.write(f'{times}\n')
        self.text_widget.insert(tk.END, f'{times}\n')

    def quit(self):
        self.cap.release()
        self.file.close()
        self.window.destroy()


#%%

# =============================================================================   
# Specify the camera source (0 is the default camera) 
# we might need to specify different kind of address to external device
# =============================================================================
video_source = 1

# =============================================================================
# # Create the Tkinter window and pass the camera source
# =============================================================================
app = CameraApp(tk.Tk(), "Camera_feed", video_source)