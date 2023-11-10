from tkinter import *

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import functions as func # my functions get and post
class Model():
    def __init__(self):
        self.dividens_list = []
        self.stock_names_list = []
      

 
    
class mainView():
    def __init__(self, root, controller): # master is the parent element of view
        self.controller = controller
        self.root = root
        self.root.configure(bg='#1D1D20')
        self.root.resizable(False, False)  # This code helps to disable windows from resizing
        self.root_height = 500
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

        self.guide_text = tk.Label(self.guide_frame,text="Here in the app you can make these actions:\n\n1- Search Dividends\t\t\n2- Save Dividends\t\t\t\n3- Generate Excel Table of Dividends\n4 - Get the last dividends search\t",bg="#1D1D20",  font= ("Roboto", 13, "bold"),  fg="white")
        self.guide_text.pack()
        
        self.buttons_frame = tk.Label(self.root,bg="#1D1D20", height=10)
        self.buttons_frame.pack(fill="x", pady=20)
        
        self.search_button = tk.Button(self.buttons_frame, text="Search Dividends", width=20, bg="#90EE90", font= ("Roboto", 11, "bold"))
        self.search_button.pack(side="left",padx=(40,0))
        self.search_button.bind("<Button>", controller.search_dividends)
        
        self.save_button = tk.Button(self.buttons_frame, text="Save Dividends", width=20, bg="#089A4F", font= ("Roboto", 11, "bold"))
        self.save_button.pack(side="left", padx=(50 ,50))
        self.save_button.bind("<Button>", controller.save_dividends)
        
        self.generate_button = tk.Button(self.buttons_frame, text="Generate Table", width=20, bg="#08FF08", font= ("Roboto", 11, "bold"))
        self.generate_button.pack(side="right",padx=(0,40))
        self.generate_button.bind("<Button>", controller.generate_exel_table)

        
        self.last_search_button = tk.Button(self.root, text="Results of last search", width=20, bg="yellow", font= ("Roboto", 11, "bold"))
        self.last_search_button.pack(padx=(50,0), pady=20)
        self.last_search_button.bind("<Button>", controller.show_last_results)
        


        self.exit_button = tk.Button(self.root, text="Exit", width=20, bg="#FF3333", font= ("Roboto", 11, "bold"))
        self.exit_button.pack(padx=(50,0), pady=(30,0))
        self.exit_button.bind("<Button>", controller.exit_window)


        
      
class Controller():       
    def __init__(self):
        self.root = tk.Tk() # root window
        self.view = mainView(self.root, self) 
        self.root.title("Stock Dividends Retriever App")
        self.dividends_list = []
        self.stock_names = []
        self.root.mainloop() # loop events listener    
        

        
    def search_dividends(self, event):
        result = messagebox.askquestion("Form", "Are you sure you want to search dividends ?")
        
        if result == 'yes':
            self.stock_names = func.get_stock_names()
            self.dividends_list = func.get_dividends(self.stock_names)
    
            
            
            message = ''
            
            
            if len(self.dividends_list) > 0:
                for i in range(len(self.dividends_list)):
                    message += f'{i + 1} - {self.stock_names[i]} : {self.dividends_list[i]}\n'
                messagebox.showinfo("List of dividends",message)   
            else:
                messagebox.showerror("Error","There is no dividends !")   
        
        
    def save_dividends(self, event):
        post_success = False
        
        post_success = func.post_diviends(self.dividends_list)
        
        if post_success:
            messagebox.showinfo("Success","Divends Registered Successfully ")
        else:
            messagebox.showerror("Error","Dividends can't be registered before the search!")
            
    def show_last_results(self, event):
        
        if len(self.dividends_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
        else:
            message = ''
            for i in range(len(self.dividends_list)):
                message += f'{i + 1} - {self.stock_names[i]} : {self.dividends_list[i]}\n'
            messagebox.showinfo("Dividends List", message)
            
    def generate_exel_table(self, event):
        if len(self.dividends_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
        else:
            func.generate_exel_file(self.stock_names, self.dividends_list)
            messagebox.showinfo("Success", "The file was created on your downloads !")
            
        
    def exit_window(self, event):
        self.root.destroy()
        





if __name__ == '__main__':
    controller = Controller()