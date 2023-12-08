import tkinter as tk
from tkinter import ttk, messagebox
import threading
import functions as func

class Model():
    def __init__(self):
        self.dividends_list = []
        self.stock_names_list = []




class LoadingView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller
        self.root = root
        self.title("Loading")
        self.root_height = 150
        self.root_width = 300
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_cordinate = int((self.screen_width/2) - (self.root_width/2))
        y_cordinate = int((self.screen_height/2) - (self.root_height/2))  
        self.geometry("{}x{}+{}+{}".format(self.root_width, self.root_height, x_cordinate, y_cordinate))
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False,self.logo )

        self.loading_label = tk.Label(self, text="I'm still searching, hang on", font=("Roboto", 12))
        self.loading_label.pack(pady=10)

        self.loading_bar = ttk.Progressbar(self, mode='indeterminate')
        self.loading_bar.pack()

        self.withdraw()  # Hide initially

    def disable_close(self):
        # Prevent closing the loading view
        pass

    def show(self):
        self.grab_set()  # Grab the focus to block interactions with the main view
        self.deiconify()

    def hide(self):
        self.grab_release()  # Release the focus to allow interactions with the main view
        self.withdraw()

class mainView():
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.configure(bg='#1D1D20')
        self.root.resizable(False, False)
        self.root_height = 500
        self.root_width = 700
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_cordinate = int((self.screen_width/2) - (self.root_width/2))
        y_cordinate = int((self.screen_height/2) - (self.root_height/2))
        self.root.geometry("{}x{}+{}+{}".format(self.root_width, self.root_height, x_cordinate, y_cordinate))

        self.label = tk.Label(text="Welcome to \nStock Dividends Retriever App", bg='#1D1D20',
                              font=("Roboto", 20, "bold"), fg="#2BABE2")
        self.label.pack(side="top", pady=10)

        self.mainFrame = tk.Frame(self.root, width=300, height=200, bg="#1D1D20")
        self.mainFrame.pack()

        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.limg = tk.Label(self.mainFrame, image=self.logo, bg="#1D1D20")
        self.limg.pack(side="right", padx=(40, 0))

        self.root.wm_iconphoto(False, self.logo)

        self.guide_frame = tk.Frame(self.mainFrame, bg='#1D1D20')
        self.guide_frame.pack()

        self.guide_title = tk.Label(self.guide_frame, text="Guide", bg="#1D1D20",
                                    font=("Roboto", 15, "bold"), fg="#FF3333")
        self.guide_title.pack(side="top", padx=90)

        self.guide_text = tk.Label(self.guide_frame, text="Here in the app you can make these actions:\n\n"
                                                           "1- Search Dividends\t\t\n"
                                                           "2- Save Dividends\t\t\t\n"
                                                           "3- Generate Excel Table of Dividends\n"
                                                           "4- Get the last dividends search\t",
                                   bg="#1D1D20", font=("Roboto", 13, "bold"), fg="white")
        self.guide_text.pack()
        


        self.buttons_frame = tk.Label(self.root, bg="#1D1D20", height=10)
        self.buttons_frame.pack(fill="x", pady=20)

        self.search_button = tk.Button(self.buttons_frame, text="Search Dividends", width=20, bg="#90EE90",activebackground="#90EE90",
                                       font=("Roboto", 11, "bold"))
        self.search_button.pack(side="left", padx=(40, 0))
        self.search_button.bind("<Button>", controller.search_dividends)

        self.save_button = tk.Button(self.buttons_frame, text="Save Dividends", width=20, bg="#089A4F",activebackground="#089A4F",
                                     font=("Roboto", 11, "bold"))
        self.save_button.pack(side="left", padx=(50, 50))
        self.save_button.bind("<Button>", controller.save_dividends)

        self.generate_button = tk.Button(self.buttons_frame, text="Generate Table", width=20, bg="#08FF08",activebackground="#08FF08",
                                         font=("Roboto", 11, "bold"))
        self.generate_button.pack(side="right", padx=(0, 40))
        self.generate_button.bind("<Button>", controller.generate_excel_table)

        self.last_search_button = tk.Button(self.root, text="Results of last search", width=20, bg="yellow",activebackground="yellow",
                                            font=("Roboto", 11, "bold"))
        self.last_search_button.pack(padx=(50, 0), pady=20)
        self.last_search_button.bind("<Button>", controller.show_last_results)

        self.exit_button = tk.Button(self.root, text="Exit", width=20, bg="#FF3333",activebackground="#FF3333",
                                     font=("Roboto", 11, "bold"))
        self.exit_button.pack(padx=(50, 0), pady=(30, 0))
        self.exit_button.bind("<Button>", controller.exit_window)

        self.loading_view = LoadingView(self.root, controller)


    def show_loading_bar(self):
        self.loading_view.show()
        self.loading_view.loading_bar.start()

    def hide_loading_bar(self):
        self.loading_view.loading_bar.stop()
        self.loading_view.hide()

class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.view = mainView(self.root, self)
        self.root.title("Stock Dividends Retriever App")
        self.dividends_list = []
        self.stock_names = []
        self.root.mainloop()

    def show_loading_bar(self):
        self.view.show_loading_bar()

    def hide_loading_bar(self):
        self.view.hide_loading_bar()

    def check_completion(self):
        if not any(thread.is_alive() for thread in threading.enumerate()):
            self.hide_loading_bar()
        else:
            self.root.after(100, self.check_completion)

    def get_dividends_thread(self):
        self.dividends_list = func.get_dividends_google_data(self.stock_names)

        message = ''

        if len(self.dividends_list) > 0:
            for i in range(len(self.dividends_list)):
                message += f'{i + 1} - {self.stock_names[i]} : {self.dividends_list[i]}\n'
            messagebox.showinfo("List of dividends", message)
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_dividends(self, event):
        result = messagebox.askquestion("Form", "Are you sure you want to search dividends ?")

        if result == 'yes':
            self.show_loading_bar()
            self.stock_names.clear()
            self.dividends_list.clear()
            success = func.get_stock_names(self.stock_names)
            if not success:
                self.hide_loading_bar()
                messagebox.showerror("Error", "The token.json file is missing!")
                return

            threading.Thread(target=self.get_dividends_thread).start()
            self.root.after(100, self.check_completion)

    def save_dividends(self, event):
        post_success = func.post_diviends(self.dividends_list)

        if post_success:
            messagebox.showinfo("Success", "Dividends Registered Successfully ")
        else:
            messagebox.showerror("Error", "Dividends can't be registered before the search!")

    def show_last_results(self, event):
        if len(self.dividends_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
        else:
            message = ''
            for i in range(len(self.dividends_list)):
                message += f'{i + 1} - {self.stock_names[i]} : {self.dividends_list[i]}\n'
            messagebox.showinfo("Dividends List", message)

    def generate_excel_table(self, event):
        if len(self.dividends_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to create a table!")
        else:
            func.generate_excel_file(self.stock_names, self.dividends_list)
            messagebox.showinfo("Success", "The file was created on your downloads !")

    def exit_window(self, event):
        self.root.destroy()

if __name__ == '__main__':
    controller = Controller()
