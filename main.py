from tkinter import *

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Model():
    def __init__(self):
        self.dividens_list = []
        self.stock_names_list = []
        pass

 
    
class mainView():
    def __init__(self, root, controller): # master is the parent element of view
        self.controller = controller
        self.root = root
        self.root.configure(bg='#1D1D20')
        self.root.resizable(False, False)  # This code helps to disable windows from resizing
        self.root_height = 400
        self.root_width = 700
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_cordinate = int((self.screen_width/2) - (self.root_width/2))
        y_cordinate = int((self.screen_height/2) - (self.root_height/2))
        self.root.geometry("{}x{}+{}+{}".format(self.root_width, self.root_height, x_cordinate, y_cordinate))


        self.label = tk.Label( text="Welcome to \nStock Dividends Retriever App",bg='#1D1D20', font= ("Roboto", 20, "bold"), fg="#2BABE2")
        self.label.pack(side="top", pady=10 )
   
        self.mainFrame = tk.Frame(self.root, width=300, height=200, bg="#1D1D20")
        self.mainFrame.pack()
        

        
        
        
                # logo image
        self.logo = tk.PhotoImage(file="img\logo.ppm" )
        self.limg = tk.Label(self.mainFrame, image=self.logo, bg="#1D1D20")
        self.limg.pack(side="right", padx=(40,0))
        
        self.guide_frame = tk.Frame(self.mainFrame, bg='#1D1D20' )
        self.guide_frame.pack()
        
        
        self.guide_title = tk.Label(self.guide_frame, text="Guide", bg="#1D1D20", font= ("Roboto", 15, "bold"),  fg="#FF3333")
        self.guide_title.pack(side="top", padx=90)

        self.guide_text = tk.Label(self.guide_frame,text="Here in the app you can make these actions:\n\n1- Search Dividends\t\t\n2- Save Dividends\t\t\t\n3- Generate Excel Table of Dividends\n",bg="#1D1D20",  font= ("Roboto", 13, "bold"),  fg="white")
        self.guide_text.pack()
        
        self.buttons_frame = tk.Label(self.root,bg="#1D1D20", height=10)
        self.buttons_frame.pack(fill="x", pady=40)
        
        self.search_button = tk.Button(self.buttons_frame, text="Search Dividends", width=20, bg="#90EE90", font= ("Roboto", 11, "bold"))
        self.search_button.pack(side="left",padx=(40,0))
        
        self.save_button = tk.Button(self.buttons_frame, text="Save Dividends", width=20, bg="#089A4F", font= ("Roboto", 11, "bold"))
        self.save_button.pack(side="left", padx=(50 ,50))
        
        self.generate_button = tk.Button(self.buttons_frame, text="Generate Table", width=20, bg="#08FF08", font= ("Roboto", 11, "bold"))
        self.generate_button.pack(side="right",padx=(0,40))

        



        
      
class Controller():       
    def __init__(self):
        self.root = tk.Tk() # root window
        self.view = mainView(self.root, self) 
        self.root.title("Stock Dividends Retriever App")
    
        self.root.mainloop() # loop events listener    
        







if __name__ == '__main__':
    controller = Controller()