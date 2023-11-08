import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Model():
    def __init__(self):
        self.dividens_list = []
        self.stock_names_list = []
        pass

 
    
class View():
    def __init__(self, master, controller): # master is the parent element of view
        self.controller = controller
        self.frame = tk.Frame(master)
        self.frame.pack()

      
class Controller():       
    def __init__(self):
        self.root = tk.Tk() # root window
        self.root.geometry('400x400')
        self.view = View(self.root, self) 
        self.root.title("Stock Dividends Retriever App")
        self.root.mainloop() # loop events listener

        
        







if __name__ == '__main__':
    controller = Controller()