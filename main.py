import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import os.path
import pickle
import functions as func
from datetime import datetime



class Stock:
    def __init__(self, name, dividend_google = None, dividend_invest10 =  None, price_to_earnings = None, price_to_book = None):
        self.name = name
        self.dividend_google = dividend_google
        self.dividend_invest10 = dividend_invest10
        self.price_to_earnings = price_to_earnings
        self.price_to_book = price_to_book
        
        
    def __str__(self):
        return f'{self.name} : {self.dividend_google} : {self.dividend_invest10} : {self.price_to_earnings}'
    
class SearchResult:
    def __init__(self, stocks):

        self.stocks = stocks
        self.date_of_search = datetime.now()
        print(f"date: {self.date_of_search}")

        

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
        

class ShowResultsView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        print(f"Screen width: {self.screen_width}")
        print(type(self.screen_width))
        
        self.frame_height = 650
        self.frame_width = 600
        x_cordinate = int((self.screen_width/2) - (self.frame_width/2))
        y_cordinate = int((self.screen_height/2) - (self.frame_height/2))
        self.geometry("{}x{}+{}+{}".format(self.frame_width, self.frame_height, x_cordinate, y_cordinate))
        self.title("Results of Search")
        
        self.text_widget = tk.Text(self, wrap=tk.WORD, width=70, height=40) 
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        
        self.text_widget.place(relx=.5, rely=.5,anchor="center")

        # last_result = self.controller.search_results[0]
        # self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        # self.add_centered_text(f"----------------------------------------\n")
        # for stock in last_result.stocks:
        #     self.add_centered_text(f"Stock Name: {stock.name}\n")
        #     self.add_centered_text(f"Dividend Google: {stock.dividend_google}\n")
        #     self.add_centered_text(f"Dividend Invest10: {stock.dividend_invest10}\n")
        #     self.add_centered_text(f"Price to Earnings: {stock.price_to_earnings}\n")
        #     self.add_centered_text(f"----------------------------------------\n")
            
        # self.text_widget.config(state="disabled")
        
        # # Insert some sample text
        # for i in range(10):
        #     self.add_centered_text(f"This is line {i+1}\nThe next will be {i +2}\n\n")
            
        # self.text_widget.config(state="disabled")
        
        
    def add_centered_text(self, text):
        # Configure a tag for centering
        self.text_widget.tag_configure("center", justify="center")

        # Insert the text with the "center" tag at the end of the widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text, "center")

        # Disable further editing
        self.text_widget.config(state=tk.DISABLED)
        
        
    def show_all_data(self, search_result):
        # print(f"tamanho :{len(self.controller.search_results)}")
        
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            
            if stock.dividend_google != None:
                self.add_centered_text(f"Dividend Google: {stock.dividend_google}\n")

            if stock.dividend_invest10 != None:
                self.add_centered_text(f"Dividend Invest10: {stock.dividend_invest10}\n")
                
            if stock.price_to_earnings != None:
                self.add_centered_text(f"Price to Earnings: {stock.price_to_earnings}\n")
                
            if stock.price_to_book != None:
                self.add_centered_text(f"Price to Book: {stock.price_to_book}\n")
                
            self.add_centered_text(f"----------------------------------------\n")
            
        self.text_widget.config(state="disabled")
        
    def show_google_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Dividend: {stock.dividend_google}\n")
            self.add_centered_text(f"----------------------------------------\n")
            
        self.text_widget.config(state="disabled")
        
        
    def show_invest10_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Dividend: {stock.dividend_invest10}\n")
            self.add_centered_text(f"----------------------------------------\n")
            
        self.text_widget.config(state="disabled")
        
    def show_prices_to_book(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Price to Book: {stock.price_to_book}\n")
            self.add_centered_text(f"----------------------------------------\n")
            
        self.text_widget.config(state="disabled")
        
    def show_price_to_earnings(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Price to Earnings: {stock.price_to_earnings}\n")
            self.add_centered_text(f"----------------------------------------\n")
            
        self.text_widget.config(state="disabled")
                


class SearchResultsView(tk.Toplevel):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        tk.Toplevel.__init__(self, root)
        self.text_widget = tk.Text(self, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        


        print(f"tamanho :{len(self.controller.search_results)}")
        print(f"Last result: {self.controller.search_results[0]}")
        print(f"Last result: {self.controller.search_results[0].stocks[0].name}")
        print(f"Last result: {type(self.controller.search_results[0])}")
        # Insert buttons as window widgets in the Text widget
        
        for i in range(len(self.controller.search_results)):
            print(f"date: {self.controller.search_results[i].date_of_search}")
            button = ttk.Button(self.text_widget, text=f"{self.controller.search_results[i].date_of_search}", command=lambda i=i: self.button_clicked(self.controller.search_results[i]))
            self.text_widget.window_create(tk.END, window=button)
            self.text_widget.insert(tk.END, "\n")  # Add a newline after each button

            # Center the entire line containing the button
            line_start = f"{i + 1}.0"
            self.text_widget.tag_add(f"button_{i+1}", line_start, f"{line_start}+2l")
            self.text_widget.tag_configure(f"button_{i+1}", justify='center')
        
        self.text_widget.config(state="disabled")
        
        self.after(1, self.center_window)
        
        
    def button_clicked(self, search_result):
        print(f"clicked {search_result}")
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data(search_result)
        
    def center_window(self):
        # Update the window's geometry
        self.update_idletasks()

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position for the window to be centered
        x_position = int((screen_width - self.winfo_reqwidth()) / 2)
        y_position = int((screen_height - self.winfo_reqheight()) / 2)

        # Set the window position
        self.geometry(f"+{x_position}+{y_position}")
        
class ChooseSearchDataView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        print(f"Screen width: {self.screen_width}")
        print(type(self.screen_width))
        
        self.frame_height = 650
        self.frame_width = 600
        x_cordinate = int((self.screen_width/2) - (self.frame_width/2))
        y_cordinate = int((self.screen_height/2) - (self.frame_height/2))
        self.geometry("{}x{}+{}+{}".format(self.frame_width, self.frame_height, x_cordinate, y_cordinate))
        self.title("Search Data")
        
        self.main_frame = tk.Frame(self, width=600, height=650, bg="#1D1D20").place(relx=.5, rely=.5,anchor="center")
        
        self.button_01 = tk.Button(self, text="Search From Google", width=20, bg="#90EE90",activebackground="#90EE90",
                                     
                                        font=("Roboto", 11, "bold"), command=self.controller.search_dividends_from_google)
        self.button_01.pack(side="left", padx=(95, 0))
        
        self.button_02 = tk.Button(self, text="Search From Invest10", width=20, bg="#089A4F",activebackground="#089A4F",

                                        font=("Roboto", 11, "bold"), command=self.controller.search_dividends_from_invest10)
        self.button_02.pack(side="left", padx=(50, 50))

class mainView():
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.configure(bg='#1D1D20')
        
        self.root_height = 700
        self.root_width = 900
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_cordinate = int((self.screen_width/2) - (self.root_width/2))
        y_cordinate = int((self.screen_height/2) - (self.root_height/2))
        self.root.geometry("{}x{}+{}+{}".format(self.root_width, self.root_height, x_cordinate, y_cordinate))

        self.label = tk.Label(text="Welcome to \nStock Dividends Retriever App", bg='#1D1D20',
                              font=("Roboto", 20, "bold"), fg="#2BABE2")
        self.label.pack(side="top", pady=20)

        self.mainFrame = tk.Frame(self.root, width=900, height=200, bg="#1D1D20").place(relx=.5, rely=.5,anchor="center")
  

        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        

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
        self.guide_text.pack(side="left")
        
        self.limg = tk.Label(self.guide_frame, image=self.logo, bg="#1D1D20")
        self.limg.pack()


        self.buttons_frame = tk.Frame(self.mainFrame, bg="#1D1D20")
        self.buttons_frame.pack(pady=(50, 0))

        self.search_button = tk.Button(self.buttons_frame, text="Search Dividends", width=20, bg="#90EE90",activebackground="#90EE90",
                                       font=("Roboto", 11, "bold"), command=controller.create_search_view)
        self.search_button.pack(side="left", padx=(95, 0))


        self.search_price_to_earnings_button = tk.Button(self.buttons_frame, text="Search price to Earnings", width=20, bg="#089A4F",activebackground="#089A4F",
                                     font=("Roboto", 11, "bold"), command=controller.search_prices_to_earnings)
        self.search_price_to_earnings_button.pack(side="left", padx=(50, 50))


        self.search_price_to_book_button = tk.Button(self.buttons_frame, text="Search price to Book", width=20, bg="#08FF08",activebackground="#08FF08",
                                         font=("Roboto", 11, "bold"), command=controller.search_price_to_book)
        self.search_price_to_book_button.pack(side="right", padx=(0, 40))


        # self.last_search_button = tk.Button(self.root, text="Results of last search", width=20, bg="yellow",activebackground="yellow",
        #                                     font=("Roboto", 11, "bold"))
        # self.last_search_button.pack(padx=(50, 0), pady=20)
        # self.last_search_button.bind("<Button>", controller.show_last_results)
        
        
        self.frame_02 = tk.Frame(self.mainFrame, width=900, height=200, bg="#1D1D20")
        self.frame_02.pack(pady=(50, 0) )
        
        
        
        
        self.stock_search_button = tk.Button(self.frame_02, text="Search a Stock", width=20, bg="#0091F7",activebackground="yellow",
                                            font=("Roboto", 11, "bold"), command=controller.search_a_stock)
        self.stock_search_button.pack(side="left", padx=(50, 40))
        
        
        # teste
        self.search_all_data_button = tk.Button(self.frame_02, text="Search All Data", width=20, bg="yellow",activebackground="yellow",
                                            font=("Roboto", 11, "bold"), command=controller.search_all_data_from_all_stocks)
        self.search_all_data_button.pack()
        
        
        
        
        self.last_search_button = tk.Button(self.root, text="Search Results", width=20, bg="yellow",activebackground="yellow",
                                            font=("Roboto", 11, "bold"), command=controller.create_search_results_view)
        self.last_search_button.pack(padx=(50, 0), pady=(30, 0))
        
        
        self.generate_button = tk.Button(self.root, text="Generate Excel file", width=20, bg="yellow",activebackground="yellow",
                                            font=("Roboto", 11, "bold"), command=controller.generate_excel_table)
        self.generate_button.pack(padx=(50, 0), pady=(30, 0))

        
    
        # self.save_data_locally_button = tk.Button(self.root, text="Save All Data Locally", width=20, bg="#fdf0d5",activebackground="#fdf0d5",
        #                              font=("Roboto", 11, "bold"), command="")
        
        
        # self.save_data_locally_button.pack(padx=(50, 0), pady=(30, 0))
        
        self.save_data_sheets_button = tk.Button(self.root, text="Save All Data On Sheets", width=20, bg="#fdf0d5",activebackground="#fdf0d5",
                                     font=("Roboto", 11, "bold"), command=self.controller.save_dividends_google)
        
        
        self.save_data_sheets_button.pack(padx=(50, 0), pady=(30, 0))
 

        self.loading_view = LoadingView(self.root, controller)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        

 
    
        
        
    def on_close(self):
        self.controller.exit_window()


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
        
        if not os.path.exists('results.pickle'):
            
            self.search_results = [] # instances of SearchResult, creates one instance of SearchResult if it doesn't exist
            
        else:
            with open('results.pickle', 'rb') as f:
                self.search_results = pickle.load(f)
                
        self.temporary_stocks = [] # instances of Stock, used to store the stocks that has other attributes
        
        self.dividends_google_list = []
        self.dividends_invest10_list = []
        self.prices_to_book_list = []
        self.price_to_earnings_list = []
        
        self.stock_names_temp = []
        
        self.all_data_list = []
        
        
        
        
        self.root.mainloop()
        
    
        
    def save_search_results(self):
        if len(self.search_results) != 0:
            with open('results.pickle', 'wb') as f:
                pickle.dump(self.search_results, f)
                
    def show_last_result(self):
        if len(self.search_results) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
            return
        
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data()

    def show_loading_bar(self):
        self.view.show_loading_bar()

    def hide_loading_bar(self):
        self.view.hide_loading_bar()

    def check_completion(self):
        if not any(thread.is_alive() for thread in threading.enumerate()):
            self.hide_loading_bar()
        else:
            self.root.after(100, self.check_completion)
            
    def get_stock_names(self, stock_names):
        return func.get_stock_names(stock_names)
            
    def get_dividends_google_data(self, stock_names):
        return func.get_dividends_google_data(stock_names)
    
    def get_dividends_invest10_data(self, stock_names):
        return func.get_dividends_from_invest10(stock_names)
    
    def get_prices_to_book_data(self, stock_names):
        return func.get_price_to_book(stock_names)
    
    def get_price_to_earnings_data(self, stock_names):
        return func.get_price_to_earnings(stock_names)
    
    def post_dividends_google_data(self, dividends_google_list):
        return func.post_dividends_google_data(dividends_google_list)
    
    def generate_excel_file(self, stock_names, dividends_google_list):
        func.generate_excel_file(stock_names, dividends_google_list)
        
    def get_data_from_a_stock(self, stock_name):
        return func.get_data_from_a_stock(stock_name)
    
    def get_all_data_from_all_stocks(self, stock_names):
        return func.get_all_data_from_all_stocks(stock_names)
    
    
    def create_search_view(self):
        self.choose_search_data_view = ChooseSearchDataView(self.root, self)
        
    def create_search_results_view(self):
        if len(self.search_results) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
            return
        
        self.search_results_view = SearchResultsView(self.root, self)
        
        
        
    def search_all_data_thread(self):
        self.all_data_list.clear()
        self.all_data_list = self.get_all_data_from_all_stocks(self.stock_names_temp) # it will append the stocks thats why it starts empty
   
        
        
        if len(self.all_data_list) > 0:

            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(Stock(self.stock_names_temp[i], dividend_google=self.all_data_list[0][i], dividend_invest10=self.all_data_list[1][i], price_to_earnings=self.all_data_list[2][i], price_to_book=self.all_data_list[3][i]))
            

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()    
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_all_data(self.search_results[0])
        
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()
        
        
    def search_all_data_from_all_stocks(self):
        self.temporary_stocks = [] 
        result = messagebox.askquestion("Form", "Are you sure you want to search all data ?")

        if result == 'yes':
            print("mostra barra de carregamento")
            self.show_loading_bar()
            
            if os.path.exists('token.json'):
                self.stock_names_temp.clear()

            
            success = self.get_stock_names(self.stock_names_temp) # it will append the stocks thats why it starts empty
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno("Input", "There is no token.json file, but you can still search for a stock. Do you want to continue?", parent=self.root)
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                            
                            if stock_name == "stop":
                                self.show_loading_bar()
                                threading.Thread(target=self.search_all_data_thread).start()
                                self.root.after(100, self.check_completion)
                                break
                            
                            if stock_name == "" or stock_name ==  None:
                                messagebox.showerror("Error", "You need to input a stock name!")
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)
                            
                    else:
            
                        
                        search_last_stocks = messagebox.askyesno("Input", "There is a temporary list of stocks, do you want to search by that?", parent=self.root)
                        
                        if search_last_stocks == True: 
                            # it is used to empty the stocks that has other attributes
                            self.show_loading_bar()
                            threading.Thread(target=self.search_all_data_thread).start()
                            self.root.after(100, self.check_completion)
                            
                            
                        else:
                    
                            
                            
                            while True:
                                stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                                
                                if stock_name == "stop":
                                    self.show_loading_bar()
                                    threading.Thread(target=self.search_all_data_thread).start()
                                    self.root.after(100, self.check_completion)
                                    break
                                
                                if stock_name == "" or stock_name ==  None:
                                    messagebox.showerror("Error", "You need to input a stock name!")
                                    continue
                                else:
                                    self.stock_names_temp.append(stock_name)
                        

                
                return

            threading.Thread(target=self.search_all_data_thread).start()
            self.root.after(100, self.check_completion)
    
    
    
    def search_a_stock_thread(self, stock_name):
        list_data = self.get_data_from_a_stock(stock_name)

        result_str = ''
        for i, data in enumerate(list_data):
            result_str += f'{i + 1} - {data}\n'
        
        
        print(list_data)

        self.hide_loading_bar()
        
        self.search_results.insert(0, SearchResult([Stock(stock_name, dividend_google=list_data[0], dividend_invest10=list_data[1], price_to_earnings=list_data[2], price_to_book=list_data[3])]))    
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data(self.search_results[0])
        # messagebox.showinfo("Stock Data", result_str)
        
    
    
    
    def search_a_stock(self):
        answer = simpledialog.askstring("Input", "What's the name of the stock you want to search?", parent=self.root)

        if answer == "" or answer ==  None:
            messagebox.showerror("Error", "You need to input a stock name!")
            return
        self.show_loading_bar()

        # Start a new thread for stock search
        threading.Thread(target=self.search_a_stock_thread, args=(answer,)).start()
        
    
    
    
    
    def get_price_to_earnings_thread(self):
        
        self.price_to_earnings_list.clear()
        self.price_to_earnings_list = self.get_price_to_earnings_data(self.stock_names_temp)
          
        if len(self.price_to_earnings_list) > 0:

            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(Stock(self.stock_names_temp[i], price_to_earnings=self.price_to_earnings_list[i]))
            
                
            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_price_to_earnings(self.search_results[0])
        
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()
        
    def search_prices_to_earnings(self):
        self.temporary_stocks = []
        result = messagebox.askquestion("Form", "Are you sure you want to search prices to earnings ?")

        if result == 'yes':
            self.show_loading_bar()
            
            if os.path.exists('token.json'):
                self.stock_names_temp.clear()

            
            success = self.get_stock_names(self.stock_names_temp) # it will append the stocks thats why it starts empty
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno("Input", "There is no token.json file, but you can still search for a stock. Do you want to continue?", parent=self.root)
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                            
                            if stock_name == "stop":
                                self.show_loading_bar()
                                threading.Thread(target=self.get_price_to_earnings_thread).start()
                                self.root.after(100, self.check_completion)
                                break
                            
                            if stock_name == "" or stock_name ==  None:
                                messagebox.showerror("Error", "You need to input a stock name!")
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)
                            
                    else:
            
                        
                        search_last_stocks = messagebox.askyesno("Input", "There is a temporary list of stocks, do you want to search by that?", parent=self.root)
                        
                        if search_last_stocks == True: 
                             # it is used to empty the stocks that has other attributes
                            self.show_loading_bar()
                            threading.Thread(target=self.get_price_to_earnings_thread).start()
                            self.root.after(100, self.check_completion)
                            
                            
                        else:
                    
                            
                            
                            while True:
                                stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                                
                                if stock_name == "stop":
                                    self.show_loading_bar()
                                    threading.Thread(target=self.get_price_to_earnings_thread).start()
                                    self.root.after(100, self.check_completion)
                                    break
                                
                                if stock_name == "" or stock_name ==  None:
                                    messagebox.showerror("Error", "You need to input a stock name!")
                                    continue
                                else:
                                    self.stock_names_temp.append(stock_name)
                        

                
                return

            threading.Thread(target=self.get_price_to_earnings_thread).start()
            self.root.after(100, self.check_completion)
        
    
    
    def get_price_to_book_thread(self):
        self.prices_to_book_list.clear()
        self.prices_to_book_list = self.get_prices_to_book_data(self.stock_names_temp) # it will append the stocks thats why it starts empty
   
        
        
        if len(self.prices_to_book_list) > 0:

            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(Stock(self.stock_names_temp[i], price_to_book=self.prices_to_book_list[i]))
            
            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()    
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_prices_to_book(self.search_results[0])
        
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()
        
        
    def search_price_to_book(self):
        self.temporary_stocks = []
   
        result = messagebox.askquestion("Form", "Are you sure you want to search prices to book ?")

        if result == 'yes':
            self.show_loading_bar()
            
            if os.path.exists('token.json'):
                self.stock_names_temp.clear()

            
            success = self.get_stock_names(self.stock_names_temp) # it will append the stocks thats why it starts empty
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno("Input", "There is no token.json file, but you can still search for a stock. Do you want to continue?", parent=self.root)
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                            
                            if stock_name == "stop":
                                self.show_loading_bar()
                                threading.Thread(target=self.get_price_to_book_thread).start()
                                self.root.after(100, self.check_completion)
                                break
                            
                            if stock_name == "" or stock_name ==  None:
                                messagebox.showerror("Error", "You need to input a stock name!")
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)
                            
                    else:
            
                        
                        search_last_stocks = messagebox.askyesno("Input", "There is a temporary list of stocks, do you want to search by that?", parent=self.root)
                        
                        if search_last_stocks == True:
                            
                            self.show_loading_bar()
                            threading.Thread(target=self.get_price_to_book_thread).start()
                            self.root.after(100, self.check_completion)
                            
                            
                        else:

                            
                            while True:
                                stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                                
                                if stock_name == "stop":
                                    self.show_loading_bar()
                                    threading.Thread(target=self.get_price_to_book_thread).start()
                                    self.root.after(100, self.check_completion)
                                    break
                                
                                if stock_name == "" or stock_name ==  None:
                                    messagebox.showerror("Error", "You need to input a stock name!")
                                    continue
                                else:
                                    self.stock_names_temp.append(stock_name)
                        

                
                return

            threading.Thread(target=self.get_price_to_book_thread).start()
            self.root.after(100, self.check_completion)
            
        
        
    
      
      
    def get_invest10_dividends_thread(self):
        self.dividends_invest10_list.clear()
        self.dividends_invest10_list = self.get_dividends_invest10_data(self.stock_names_temp) # it will append the stocks thats why it starts empty

        
        if len(self.dividends_invest10_list) > 0:

            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(Stock(self.stock_names_temp[i], dividend_invest10=self.dividends_invest10_list[i]))
                
            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_invest10_dividends(self.search_results[0])
        
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()
        
        
    def search_dividends_from_invest10(self):
        self.temporary_stocks = []
        self.choose_search_data_view.destroy()
        result = messagebox.askquestion("Form", "Are you sure you want to search dividends ?")

        if result == 'yes':
            self.show_loading_bar()
            
            if os.path.exists('token.json'):
                self.stock_names_temp.clear()

            
            success = self.get_stock_names(self.stock_names_temp) # it will append the stocks thats why it starts empty
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno("Input", "There is no token.json file, but you can still search for a stock. Do you want to continue?", parent=self.root)
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                            
                            if stock_name == "stop":
                                self.show_loading_bar()
                                threading.Thread(target=self.get_invest10_dividends_thread).start()
                                self.root.after(100, self.check_completion)
                                break
                            
                            if stock_name == "" or stock_name ==  None:
                                messagebox.showerror("Error", "You need to input a stock name!")
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)
                            
                    else:
            
                        
                        search_last_stocks = messagebox.askyesno("Input", "There is a temporary list of stocks, do you want to search by that?", parent=self.root)
                        
                        if search_last_stocks == True:
                            
                            self.show_loading_bar()
                            threading.Thread(target=self.get_invest10_dividends_thread).start()
                            self.root.after(100, self.check_completion)
                            
                            
                        else:
                      
                            
                            while True:
                                stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                                
                                if stock_name == "stop":
                                    self.show_loading_bar()
                                    threading.Thread(target=self.get_invest10_dividends_thread).start()
                                    self.root.after(100, self.check_completion)
                                    break
                                
                                if stock_name == "" or stock_name ==  None:
                                    messagebox.showerror("Error", "You need to input a stock name!")
                                    continue
                                else:
                                    self.stock_names_temp.append(stock_name)
                        

                
                return

            threading.Thread(target=self.get_invest10_dividends_thread).start()
            self.root.after(100, self.check_completion)
          
        
        
    
    
    def get_google_dividends_thread(self):
        
        self.dividends_google_list.clear()
        self.dividends_google_list = self.get_dividends_google_data(self.stock_names_temp) # it will append the stocks thats why it starts empty
        
        message = ''

        if len(self.dividends_google_list) > 0:

            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(Stock(self.stock_names_temp[i], dividend_google=self.dividends_google_list[i]))
                
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_google_dividends(self.search_results[0])
        
        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_dividends_from_google(self):
        self.temporary_stocks = []
        self.choose_search_data_view.destroy()
        result = messagebox.askquestion("Form", "Are you sure you want to search dividends ?")

        if result == 'yes':
            self.show_loading_bar()
            
            if os.path.exists('token.json'):
                self.stock_names_temp.clear()
     
            
            success = self.get_stock_names(self.stock_names_temp) # it will append the stocks thats why it starts empty
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno("Input", "There is no token.json file, but you can still search for a stock. Do you want to continue?", parent=self.root)
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                            
                            if stock_name == "stop":
                                self.show_loading_bar()
                                threading.Thread(target=self.get_google_dividends_thread).start()
                                self.root.after(100, self.check_completion)
                                break
                            
                            if stock_name == "" or stock_name ==  None:
                                messagebox.showerror("Error", "You need to input a stock name!")
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)
                            
                    else:
            
                        
                        search_last_stocks = messagebox.askyesno("Input", "There is a temporary list of stocks, do you want to search by that?", parent=self.root)
                        
                        if search_last_stocks == True:
                            
                            self.show_loading_bar()
                            threading.Thread(target=self.get_google_dividends_thread).start()
                            self.root.after(100, self.check_completion)
                            
                            
                        else:
                            
                            
                            while True:
                                stock_name = simpledialog.askstring("Input", "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'", parent=self.root)
                                
                                if stock_name == "stop":
                                    self.show_loading_bar()
                                    threading.Thread(target=self.get_google_dividends_thread).start()
                                    self.root.after(100, self.check_completion)
                                    break
                                
                                if stock_name == "" or stock_name ==  None:
                                    messagebox.showerror("Error", "You need to input a stock name!")
                                    continue
                                else:
                                    self.stock_names_temp.append(stock_name)
                        

                
                return

            threading.Thread(target=self.get_google_dividends_thread).start()
            self.root.after(100, self.check_completion)
            
            


    def save_dividends_google(self):
        if not os.path.exists('token.json'):
            messagebox.showerror("Error", "There is no token.json file, you can't save it to google sheets!")
            return
        
        post_success = self.post_dividends_google_data(self.dividends_google_list)

        if post_success:
            messagebox.showinfo("Success", "Dividends Registered Successfully ")
    
        else:
            messagebox.showerror("Error", "Dividends can't be registered before the search!")

    def show_last_results(self):
        if len(self.dividends_google_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to get the last results!")
        else:
            message = ''
            for i in range(len(self.dividends_google_list)):
                message += f'{i + 1} - {self.stock_names_temp[i]} : {self.dividends_google_list[i]}\n'
            messagebox.showinfo("Dividends List", message)

    def generate_excel_table(self):
        if len(self.dividends_google_list) == 0:
            messagebox.showinfo("Empty List", "You need to search for at least one time to create a table!")
        else:
            self.generate_excel_file(self.stock_names_temp, self.dividends_google_list)
            messagebox.showinfo("Success", "The file was created on your downloads !")

    def exit_window(self):
        
        # last_result = SearchResult()
        # last_result.stocks = self.temporary_stocks
        
        # if len(self.temporary_stocks) > 0:
        #     self.search_results.append(last_result)
        
        self.root.destroy()
        # self.save_search_results()

if __name__ == '__main__':
    controller = Controller()
