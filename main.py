import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import os.path
import pickle

import datetime


from datetime import datetime


import functions as func
import send_email as sd


class Stock:
    def __init__(
        self,
        name,
        dividend_google=None,
        dividend_invest10=None,
        price_to_earnings=None,
        price_to_book=None,
    ):
        self.name = name
        self.dividend_google = dividend_google
        self.dividend_invest10 = dividend_invest10
        self.price_to_earnings = price_to_earnings
        self.price_to_book = price_to_book

    def __str__(self):
        return f"{self.name} : {self.dividend_google} : {self.dividend_invest10} : {self.price_to_earnings}"


class SearchResult:
    def __init__(self, stocks):
        self.stocks = stocks
        self.date_of_search = datetime.now()


class PotentialStockToBuy:
    def __init__(self, name, real_time_price, target_price):
        self.name = name
        self.real_time_price = real_time_price
        self.target_price = target_price


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
        x_cordinate = int((self.screen_width / 2) - (self.root_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.root_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.root_width, self.root_height, x_cordinate, y_cordinate
            )
        )
        self.configure(bg="#1c1830")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)

        self.loading_label = tk.Label(
            self, text="Searching Data...", font=("Roboto", 12), fg="white", bg="#1c1830"
        )
        self.loading_label.pack(pady=10)

        self.loading_bar = ttk.Progressbar(self, mode="indeterminate")
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

        self.frame_height = 400
        self.frame_width = 600
        x_cordinate = int((self.screen_width / 2) - (self.frame_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.frame_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.frame_width, self.frame_height, x_cordinate, y_cordinate
            )
        )
        self.title("Results of Search")
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)
        self.text_widget = tk.Text(self, wrap=tk.WORD, width=70, height=22)
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)


    def add_centered_text(self, text):
        # Configure a tag for centering
        self.text_widget.tag_configure("center", justify="center")
        # Insert the text with the "center" tag at the end of the widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text, "center")
        # Disable further editing
        self.text_widget.config(state=tk.DISABLED)

    def show_all_data(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")

            if stock.dividend_google != None:
                self.add_centered_text(
                    f"Dividend Yield From Google: {stock.dividend_google} \n")

            if stock.dividend_invest10 != None:
                self.add_centered_text(
                    f"Dividend Yield from Invest10: {stock.dividend_invest10}\n"
                )

            if stock.price_to_earnings != None:
                self.add_centered_text(
                    f"Share Price / Earnings per Share:  {stock.price_to_earnings}\n"
                )

            if stock.price_to_book != None:
                self.add_centered_text(
                    f"Share Price / Book Value per Share:  {stock.price_to_book}\n")

            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_google_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Dividend Yield {stock.dividend_google}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_invest10_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Dividend Yield {stock.dividend_invest10}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_prices_to_book(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(
                f"Share Price / Book Value per Share:  {stock.price_to_book}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_price_to_earnings(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(
                f"Share Price / Earnings per Share:  {stock.price_to_earnings}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")
        
class ShowUserGuideView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.frame_height = 400
        self.frame_width = 600
        x_cordinate = int((self.screen_width / 2) - (self.frame_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.frame_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.frame_width, self.frame_height, x_cordinate, y_cordinate
            )
        )
        self.title("User Guide")
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)
        self.text_widget = tk.Text(self, wrap=tk.WORD, width=70, height=22)
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    def add_centered_text(self, text):
        # Configure a tag for centering
        self.text_widget.tag_configure("center", justify="center")
        # Insert the text with the "center" tag at the end of the widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text, "center")
        # Disable further editing
        self.text_widget.config(state=tk.DISABLED)



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

        

        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)

        # Insert buttons as window widgets in the Text widget
        for i in range(5):
            self.text_widget.insert(tk.END, "\n")

        for i in range(len(self.controller.search_results)):
            button = ttk.Button(
                self.text_widget,
                text=f"{self.controller.search_results[i].date_of_search.strftime('%d/%m/%Y %H:%M')}",
                command=lambda i=i: self.button_clicked(
                    self.controller.search_results[i]
                ),
                cursor="hand2",
            )

            self.text_widget.window_create(tk.END, window=button)
            # Add a newline after each button
            self.text_widget.insert(tk.END, "  ")
            if (i+1) % 5 == 0 and i != 0:
                self.text_widget.insert(tk.END, "\n\n")
            # Center the entire line containing the button
            line_start = f"{i + 1}.0"
            self.text_widget.tag_add(
                f"button_{i+1}", line_start, f"{line_start}+2l")
            self.text_widget.tag_configure(f"button_{i+1}", justify="center")

        self.text_widget.config(state="disabled", background="#1c1830")


        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.frame_height = 400
        self.frame_width = 600
        x_cordinate = int((self.screen_width / 2) - (self.frame_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.frame_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.frame_width, self.frame_height, x_cordinate, y_cordinate
            )
        )
    def button_clicked(self, search_result):
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data(search_result)


class ChooseSearchDataView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.frame_height = 400
        self.frame_width = 600
        x_cordinate = int((self.screen_width / 2) - (self.frame_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.frame_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.frame_width, self.frame_height, x_cordinate, y_cordinate
            )
        )
        self.title("Search Data")
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)

        self.main_frame = tk.Frame(self, width=600, height=650, bg="#1c1830").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        self.button_01 = tk.Button(
            self,
            text="Search From Google",
            width=20,
            bg="#456990",
            fg="white",
            cursor="hand2",
            activebackground="#456990",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_dividends_from_google,
        )
        self.button_01.pack(side="left", padx=(95, 0))

        self.button_02 = tk.Button(
            self,
            text="Search From Invest10",
            width=20,
            cursor="hand2",
            fg="white",
            bg="#9A2C5D",
            activebackground="#9A2C5D",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_dividends_from_invest10,
        )
        self.button_02.pack(side="left", padx=(50, 50))


class mainView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.background_image = tk.PhotoImage(file="./img/app-bg.png")

        # Create a label to hold the background image
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Raise other widgets above the background image
        self.background_label.lower()

        self.root_height = 500
        self.root_width = 900
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_cordinate = int((self.screen_width / 2) - (self.root_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.root_height / 2))
        self.root.geometry(
            "{}x{}+{}+{}".format(
                self.root_width, self.root_height, x_cordinate, y_cordinate
            )
        )

        self.label = tk.Label(
            text="Welcome to \nStock Data Watcher App",
            bg="#1c1830",
            height=0,
            font=("Roboto", 20, "bold"),
            fg="#2BABE2",

        )
        self.label.pack(side="top", pady=20)


        self.logo = tk.PhotoImage(file="./img/logo-new.ppm")

        self.root.wm_iconphoto(False, self.logo)

    
        self.guide_button = tk.Button(
            text="User Guide",
            width=20,
            bg="#C62068",
            fg="white",
            cursor="hand2",
            activebackground="#C62068",
            font=("Roboto", 11, "bold"),
            command=controller.show_user_guide,
            
        ).place(relx=0.8, rely=0.1, anchor="center")

        self.search_button = tk.Button(

            text="Search DY",
            width=20,
            bg="#1c1830",
            fg="white",
            cursor="hand2",
            activebackground="#1c1830",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_view,
        ).place(relx=0.2, rely=0.25, anchor="center")

        self.search_price_to_earnings_button = tk.Button(
            text="Search P / E",
            width=20,
            bg="#14182C",
            fg="white",
            cursor="hand2",
            activebackground="#14182C",
            font=("Roboto", 11, "bold"),
            command=controller.search_prices_to_earnings,
        ).place(relx=0.5, rely=0.25, anchor="center")

        self.search_price_to_book_button = tk.Button(

            text="Search P / B",
            width=20,
            bg="#1c1830",
            fg="white",
            cursor="hand2",
            activebackground="#1c1830",
            font=("Roboto", 11, "bold"),
            command=controller.search_price_to_book,
        ).place(relx=0.8, rely=0.25, anchor="center")

        self.stock_search_button = tk.Button(

            text="Search a Stock",
            width=20,
            bg="#293B57",
            fg="white",
            cursor="hand2",
            activebackground="#293B57",
            font=("Roboto", 11, "bold"),
            command=controller.search_a_stock,
        ).place(relx=0.35, rely=0.4, anchor="center")

        self.search_all_data_button = tk.Button(

            text="Search All Data",
            width=20,
            bg="#293B57",
            fg="white",
            activebackground="#293B57",
            cursor="hand2",
            font=("Roboto", 11, "bold"),
            command=controller.search_all_data_from_all_stocks,
        ).place(relx=0.65, rely=0.4, anchor="center")

        self.last_search_button = tk.Button(
            text="Search Results",
            width=20,
            bg="#456990",
            fg="white",
            cursor="hand2",
            activebackground="#456990",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_results_view,
        ).place(relx=0.5, rely=0.55, anchor="center")

        self.generate_button = tk.Button(
            text="Generate Excel file",
            width=20,
            bg="#9A2C5D",
            fg="white",
            cursor="hand2",
            activebackground="#9A2C5D",
            font=("Roboto", 11, "bold"),
            command=controller.generate_excel_table,
        ).place(relx=0.5, rely=0.65, anchor="center")

        self.save_data_sheets_button = tk.Button(
            text="Save All Data On Sheets",
            width=20,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.save_all_data_on_sheets,
        ).place(relx=0.5, rely=0.75, anchor="center")
        
        
        self.create_a_stock_list_button = tk.Button(
            text="Create a Stock List",
            width=20,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.create_stock_list,
        ).place(relx=0.5, rely=0.85, anchor="center")

        self.loading_view = LoadingView(self.root, controller)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.controller.exit_window()
        
        

    def show_loading_bar(self):
        self.loading_view.show()
        self.loading_view.loading_bar.start()
        self.controller.loading_event.set()

    def hide_loading_bar(self):
        self.loading_view.loading_bar.stop()
        self.loading_view.hide()
        self.controller.loading_event.clear()


class Controller:
    def __init__(self):
        self.root = tk.Tk()

        self.view = mainView(self.root, self)
        self.root.title("Stock Data Watcher App")
        self.icon = tk.PhotoImage(file="./img/logo.ppm")
        if not os.path.exists("results.pickle"):
            # instances of SearchResult, creates one instance of SearchResult if it doesn't exist
            self.search_results = []

        else:
            with open("results.pickle", "rb") as f:
                self.search_results = pickle.load(f)
                

        if not os.path.exists("potential-stocks-to-buy.pickle"):
            self.potential_stocks_to_buy = []

        else:
            with open("potential-stocks-to-buy.pickle", "rb") as f:
                self.potential_stocks_to_buy = pickle.load(f)
                
        if not os.path.exists("stocks-list.pickle"):
            self.stock_names_temp = []
            
        else:
            if not os.path.exists("token.json"):
                with open("stocks-list.pickle", "rb") as f:
                    self.stock_names_temp = pickle.load(f)

        # instances of Stock, used to store the stocks that has other attributes
        self.temporary_stocks = []

        self.dividends_google_list = []
        self.dividends_invest10_list = []
        self.prices_to_book_list = []
        self.price_to_earnings_list = []

       

        self.all_data_list = []

        self.temporary_potential_stocks = []

        # Event to signal the thread to exit
        self.exit_event = threading.Event()
        self.loading_event = threading.Event()

        self.already_check_stock_prices = False

        # # Periodically check for the exit condition in the main thread
        self.root.after(1000, self.repeating_function)
        self.check_exit_condition()

        self.root.mainloop()

    def repeating_function(self):
        print("Checking time to search stock's new prices!")
        if (
            (datetime.now().minute) % 10 == 0 # every 10 minutes
            and not self.exit_event.is_set()
            and not self.loading_event.is_set()
            and not self.already_check_stock_prices
        ):
            self.root.after(0, self.track_daily_prices)
            self.root.after(10000, self.track_daily_prices)
            self.already_check_stock_prices = True

        if (datetime.now().minute) % 10 != 0:
            self.already_check_stock_prices = False
        # Schedule the function to run again in 10 seconds
        self.root.after(10000, self.repeating_function)
        
    def save_stock_list(self): # only is called in case the user doesnt have a token.json file
        if len(self.stock_names_temp) != 0:
            with open("stocks-list.pickle", "wb") as f:
                pickle.dump(self.stock_names_temp, f)

    def save_search_results(self):
        if len(self.search_results) != 0:
            with open("results.pickle", "wb") as f:
                pickle.dump(self.search_results, f)

    def save_potential_stocks_to_buy(self):
        if len(self.potential_stocks_to_buy) != 0:
            with open("potential-stocks-to-buy.pickle", "wb") as f:
                pickle.dump(self.potential_stocks_to_buy, f)
                
    def show_user_guide(self):
        user_guide = (
        "Welcome to the Data Watcher App!\n\n"
        "This app is designed with the primary goal of assisting investors in making informed decisions "
        "about stock investments. It leverages various parameters provided by the Stock Exchange to offer strategic insights "
        "into potential investment opportunities. Users can access key information through functionalities such as:\n\n"
        "1. Dividend Yield Search: Obtain dividend yield data from two distinct sources—Google and Investidor10.\n"
        "2. Price-to-Earnings Ratio Search: Evaluate the stock's value by searching its Price divided by Earnings.\n"
        "3. Price-to-Assets Ratio Search: Assess the financial health of the company by searching its Price divided by the total assets.\n\n"
        "In addition to these features, users can conveniently track their search history for comparison purposes. "
        "The app also enables the generation of an Excel file containing all the searched information.\n\n"
        "Another noteworthy functionality is the seamless integration with Google Sheets. When logged into your Google account, "
        "you can update a cloud-based Google Sheets file and retrieve parameters stored within it. If not logged in, "
        "the app allows you to create and store your personalized stock list for future reference."
    )
        self.show_user_guide_view = ShowUserGuideView(self.root, self)
        self.show_user_guide_view.add_centered_text(user_guide)
        
        

    def show_last_result(self):
        if len(self.search_results) == 0:
            messagebox.showinfo(
                "Empty List",
                "You need to search for at least one time to get the last results!"
            )
            return

        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data()
        
    def create_stock_list(self):
        print(self.stock_names_temp)
        if len(self.stock_names_temp) > 0 :
            answer = messagebox.askyesno(
                "Existent List",
                "You already have a stock list, if you want to create a new one, the last stock list will be deleted!"
            )
            
            if answer == True:
                self.stock_names_temp = []
                while True:
                    stock = simpledialog.askstring(
                    "Input",
                    "What's the name of the stock you want to add?\n If you don't wanna add more stocks just type 'stop'",
                    parent=self.root,
                )
                    if stock == None and len(self.stock_names_temp) == 0:
                        return
                    if stock == "stop" and len(self.stock_names_temp) == 0:
                        return
                    
                    if stock == "stop" and len(self.stock_names_temp) > 0:
                        return
                    
                    if (stock == "" or stock == None) and len(self.stock_names_temp) == 0:
                        messagebox.showerror("Error", "You need to input a stock name!")
                        continue
                    
                    if stock != "stop" and stock != None and stock != "":
                        self.stock_names_temp.append(stock)
                        
                
        else:
            while True:
                stock = simpledialog.askstring(
                "Input",
                "What's the name of the stock you want to add?\n If you don't wanna add more stocks just type 'stop'",
                parent=self.root,
            )
                if stock == None and len(self.stock_names_temp) == 0:
                        return
                if stock == "stop" and len(self.stock_names_temp) == 0:
                    return
                
                if stock == "stop" and len(self.stock_names_temp) > 0:
                    return
                
                if (stock == "" or stock == None) and len(self.stock_names_temp) == 0:
                    messagebox.showerror("Error", "You need to input a stock name!")
                    continue
                
                if stock != "stop" and stock != None and stock != "":
                    self.stock_names_temp.append(stock)
            
            

    def show_loading_bar(self):
        self.view.show_loading_bar()

    def hide_loading_bar(self):
        self.view.hide_loading_bar()

    def check_completion(self):
        if not any(thread.is_alive() for thread in threading.enumerate()):
            self.hide_loading_bar()
        else:
            self.root.after(100, self.check_completion)

    def get_dividends_google_data(self, stock_names):
        return func.get_dividends_google_data(stock_names)

    def get_dividends_invest10_data(self, stock_names):
        return func.get_dividends_from_invest10(stock_names)

    def get_prices_to_book_data(self, stock_names):
        return func.get_price_to_book(stock_names)

    def get_price_to_earnings_data(self, stock_names):
        return func.get_price_to_earnings(stock_names)

    def post_data_list(self, dividends_google_list, DY_COLUMN_UPDATE_GOOGLE):
        return func.post_data_list(dividends_google_list, DY_COLUMN_UPDATE_GOOGLE)

    def generate_excel_file(self, stock_names, dividends_google_list, dividends_invest10_list, prices_to_book_list, price_to_earnings_list):
        func.generate_excel_file(stock_names, dividends_google_list,
                                 dividends_invest10_list, prices_to_book_list, price_to_earnings_list)

    def get_data_from_a_stock(self, stock_name):
        return func.get_data_from_a_stock(stock_name)

    def get_all_data_from_all_stocks(self, stock_names):
        return func.get_all_data_from_all_stocks(stock_names)

    def get_colum_data_from_sheets(self, list_prices, COLUMN_GET_DATA):
        return func.get_colum_data_from_sheets(list_prices, COLUMN_GET_DATA)

    def create_search_view(self):
        self.choose_search_data_view = ChooseSearchDataView(self.root, self)

    def create_search_results_view(self):
        if len(self.search_results) == 0:
            messagebox.showinfo(
                "Empty List",
                "You need to search for at least one time to get the last results!",
            )
            return

        self.search_results_view = SearchResultsView(self.root, self)

    def search_all_data_thread(self):
        self.all_data_list = []
        # it will append the stocks thats why it starts empty
        self.all_data_list = self.get_all_data_from_all_stocks(
            self.stock_names_temp)

        if len(self.all_data_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            dividend_google=self.all_data_list[0][i],
                            dividend_invest10=self.all_data_list[1][i],
                            price_to_earnings=self.all_data_list[2][i],
                            price_to_book=self.all_data_list[3][i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_all_data(self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no Data Searched!")

        self.hide_loading_bar()

    def search_all_data_from_all_stocks(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search all data ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(
                self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                if len(self.stock_names_temp) == 0:
                    while True:
                        stock_name = simpledialog.askstring(
                            "Input",
                            "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.search_all_data_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:

                            return

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Error", "You need to input a stock name!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Input",
                        "There is a temporary list of stocks, do you want to search by that?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        # it is used to empty the stocks that has other attributes
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.search_all_data_thread).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.search_all_data_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Error", "You need to input a stock name!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.search_all_data_thread).start()
            self.root.after(100, self.check_completion)

    def search_a_stock_thread(self, stock_name):
        list_data = self.get_data_from_a_stock(stock_name)

        self.hide_loading_bar()

        self.search_results.insert(
            0,
            SearchResult(
                [
                    Stock(
                        stock_name,
                        dividend_google=list_data[0],
                        dividend_invest10=list_data[1],
                        price_to_earnings=list_data[2],
                        price_to_book=list_data[3],
                    )
                ]
            ),
        )
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data(self.search_results[0])

    def search_a_stock(self):
        answer = simpledialog.askstring(
            "Input",
            "What's the name of the stock you want to search?",
            parent=self.root,
        )
        
        if answer == None:
            return

        if answer == "":
            messagebox.showerror("Error", "You need to input a stock name!")
            return
        self.show_loading_bar()

        # Start a new thread for stock search
        threading.Thread(target=self.search_a_stock_thread,
                         args=(answer,)).start()

    def get_price_to_earnings_thread(self):
        self.price_to_earnings_list = []
        self.price_to_earnings_list = self.get_price_to_earnings_data(
            self.stock_names_temp
        )

        if len(self.price_to_earnings_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            price_to_earnings=self.price_to_earnings_list[i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_price_to_earnings(
                self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no P / E !")

        self.hide_loading_bar()

    def search_prices_to_earnings(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search (Share Price / Earnings per Share) ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(
                self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                
                if len(self.stock_names_temp) == 0:
                    while True:
                        stock_name = simpledialog.askstring(
                            "Input",
                            "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_price_to_earnings_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Error", "You need to input a stock name!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Input",
                        "There is a temporary list of stocks, do you want to search by that?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        # it is used to empty the stocks that has other attributes
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_price_to_earnings_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_price_to_earnings_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Error", "You need to input a stock name!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_price_to_earnings_thread).start()
            self.root.after(100, self.check_completion)

    def get_price_to_book_thread(self):
        self.prices_to_book_list = []
        # it will append the stocks thats why it starts empty
        self.prices_to_book_list = self.get_prices_to_book_data(
            self.stock_names_temp)

        if len(self.prices_to_book_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            price_to_book=self.prices_to_book_list[i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_prices_to_book(self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no P / B !")

        self.hide_loading_bar()

    def search_price_to_book(self):
        self.temporary_stocks = []

        result = messagebox.askquestion(
            "Form", "Are you sure you want to search (Share Price / Book Value per Share) ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(
                self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                
                if len(self.stock_names_temp) == 0:
                    while True:
                        stock_name = simpledialog.askstring(
                            "Input",
                            "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_price_to_book_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Error", "You need to input a stock name!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Input",
                        "There is a temporary list of stocks, do you want to search by that?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_price_to_book_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_price_to_book_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Error", "You need to input a stock name!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_price_to_book_thread).start()
            self.root.after(100, self.check_completion)

    def get_invest10_dividends_thread(self):
        self.dividends_invest10_list = []
        self.dividends_invest10_list = self.get_dividends_invest10_data(
            self.stock_names_temp
        )  # it will append the stocks thats why it starts empty

        if len(self.dividends_invest10_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            dividend_invest10=self.dividends_invest10_list[i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_invest10_dividends(
                self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_dividends_from_invest10(self):
        self.temporary_stocks = []
        self.choose_search_data_view.destroy()
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search Dividend Yield from Invest10 ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(
                self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                
                if len(self.stock_names_temp) == 0:
                    while True:
                        stock_name = simpledialog.askstring(
                            "Input",
                            "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_invest10_dividends_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Error", "You need to input a stock name!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Input",
                        "There is a temporary list of stocks, do you want to search by that?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_invest10_dividends_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_invest10_dividends_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Error", "You need to input a stock name!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_invest10_dividends_thread).start()
            self.root.after(100, self.check_completion)

    def get_google_dividends_thread(self):
        self.dividends_google_list = []
        self.dividends_google_list = self.get_dividends_google_data(
            self.stock_names_temp
        )  # it will append the stocks thats why it starts empty

        if len(self.dividends_google_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            dividend_google=self.dividends_google_list[i],
                        )
                    )


            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_google_dividends(
                self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_dividends_from_google(self):
        self.temporary_stocks = []
        self.choose_search_data_view.destroy()
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search Dividend Yield from Google ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(
                self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                
                if len(self.stock_names_temp) == 0:
                    while True:
                        stock_name = simpledialog.askstring(
                            "Input",
                            "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_google_dividends_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Error", "You need to input a stock name!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Input",
                        "There is a temporary list of stocks, do you want to search by that?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_google_dividends_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_google_dividends_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Error", "You need to input a stock name!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_google_dividends_thread).start()
            self.root.after(100, self.check_completion)

    def compare_real_time_prices(self):
        self.stock_names_temp = []

        self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")

        self.target_price_list = []
        self.get_colum_data_from_sheets(self.target_price_list, "Página1!B3:B")

        last_row = len(self.target_price_list) + 2
        self.real_time_prices_list = []
        self.get_colum_data_from_sheets(
            self.real_time_prices_list, f"Página1!D3:D{last_row}"
        )
        
        for i in range(len(self.real_time_prices_list)):
            self.real_time_prices_list[i] = float(
                self.real_time_prices_list[i]
                .replace(",", ".")
                .replace("R$", "")
                .replace(" ", "")
            )
            self.target_price_list[i] = float(
                self.target_price_list[i]
                .replace(",", ".")
                .replace("R$", "")
                .replace(" ", "")
            )

        for i in range(len(self.real_time_prices_list)):
            if self.real_time_prices_list[i] <= self.target_price_list[i]:
                stock = self.get_stock(self.stock_names_temp[i])
                if stock == None:  # new stock that isnt in the potential stocks list
                    self.potential_stocks_to_buy.append(
                        PotentialStockToBuy(
                            self.stock_names_temp[i],
                            self.real_time_prices_list[i],
                            self.target_price_list[i],
                        )
                    )
                    self.temporary_potential_stocks.append(
                        PotentialStockToBuy(
                            self.stock_names_temp[i],
                            self.real_time_prices_list[i],
                            self.target_price_list[i],
                        )
                    )

                else:
                    if self.real_time_prices_list[i] < stock.real_time_price:
                        stock.real_time_price = self.real_time_prices_list[i]
                        stock.target_price = self.target_price_list[i]
                        self.temporary_potential_stocks.append(stock)

        if len(self.temporary_potential_stocks) > 0:
            sd.send_email("Raimundo", self.temporary_potential_stocks)
            self.temporary_potential_stocks = []

        else:
            print("There is no potential stocks to buy!")

        self.save_potential_stocks_to_buy()

    def get_stock(self, stock_name):
        for stock in self.potential_stocks_to_buy:
            if stock.name == stock_name:
                return stock

        return None

    def run_comparison_with_loading_bar(self):
        # Schedule compare_real_time_prices to run after a delay (e.g., 100 milliseconds)
        self.root.after(100, self.compare_real_time_prices)

    def track_daily_prices(self):
        if (
            not self.exit_event.is_set()
            and not self.exit_event.is_set()
            and not self.loading_event.is_set()
        ):
            self.root.after(0, self.run_comparison_with_loading_bar)

    def save_dividends_google(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_google_list, "AF")

        if post_success:
            messagebox.showinfo(
                "Success", "Dividends Registered Successfully ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def save_dividends_invest10(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_invest10_list, "AG")

        if post_success:
            messagebox.showinfo(
                "Success", "Dividends Registered Successfully ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def save_prices_to_book(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        post_success = self.post_data_list(self.prices_to_book_list, "AE")

        if post_success:
            messagebox.showinfo(
                "Success", "Dividends Registered Successfully ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def save_prices_to_earnings(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        post_success = self.post_data_list(self.price_to_earnings_list, "AD")

        if post_success:
            messagebox.showinfo(
                "Success", "Dividends Registered Successfully ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def save_dividends_google(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_google_list, "AF")

        if post_success:
            messagebox.showinfo(
                "Success", "Dividends Registered Successfully ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def show_last_results(self):
        if len(self.dividends_google_list) == 0:
            messagebox.showinfo(
                "Empty List",
                "You need to search for at least one time to get the last results!",
            )
        else:
            message = ""
            for i in range(len(self.dividends_google_list)):
                message += f"{i + 1} - {self.stock_names_temp[i]} : {self.dividends_google_list[i]}\n"
            messagebox.showinfo("Dividends List", message)

    def generate_excel_table(self):
        if len(self.all_data_list) != 0:
            self.generate_excel_file(
                self.stock_names_temp, self.all_data_list[0], self.all_data_list[1], self.all_data_list[2], self.all_data_list[3])
            messagebox.showinfo(
                "Success", "The file was created on your downloads !")
            return

        elif len(self.dividends_google_list) != 0 and len(self.dividends_invest10_list) != 0 and len(self.prices_to_book_list) != 0 and len(self.price_to_earnings_list) != 0:
            self.generate_excel_file(self.stock_names_temp, self.dividends_google_list,
                                     self.dividends_invest10_list, self.prices_to_book_list, self.price_to_earnings_list)
            messagebox.showinfo(
                "Success", "The file was created on your downloads !")
            return

        else:
            messagebox.showerror(
                "Error", "There is no sufficient data to generate a excel file!")
            return

    def save_all_data_on_sheets(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Error",
                "There is no token.json file, you can't save it to google sheets!",
            )
            return

        if (len(self.dividends_google_list) > 0 or len(self.dividends_invest10_list) > 0 or len(self.prices_to_book_list) > 0 or len(self.price_to_earnings_list) > 0) and len(self.all_data_list) == 0:
            if self.dividends_google_list:
                post_success = self.post_data_list(
                    self.dividends_google_list, "AA")

            if self.dividends_invest10_list:
                post_success = self.post_data_list(
                    self.dividends_invest10_list, "AB")

            if self.prices_to_book_list:
                post_success = self.post_data_list(
                    self.prices_to_book_list, "Z")

            if self.price_to_earnings_list:
                post_success = self.post_data_list(
                    self.price_to_earnings_list, "Y")

            if post_success:
                messagebox.showinfo(
                    "Success", "All Data was registered Successfully ")

            else:
                messagebox.showerror("Error", "Failed to save all Data!")

            return

        if len(self.all_data_list) == 0:
            messagebox.showinfo(
                "Empty List",
                "You need to search for at least one time to save all data!",
            )
            return

        # Google dividends
        # Invest10 Dividends
        # Share Price / Earnings per Share
        # Share Price / Book Value per Share

        post_success = self.post_data_list(self.all_data_list[0], "AA")
        post_success = self.post_data_list(self.all_data_list[1], "AB")
        post_success = self.post_data_list(self.all_data_list[2], "Z")
        post_success = self.post_data_list(self.all_data_list[3], "Y")

        if post_success:
            messagebox.showinfo(
                "Success", "All Data was registered Successfully ")

        else:
            messagebox.showerror("Error", "Failed to save all Data!")

    def check_exit_condition(self):
        # Periodically check for the exit condition in the main thread
        if not self.exit_event.is_set():
            # Check every second
            self.root.after(1000, self.check_exit_condition)

    def exit_window(self):
        print("exit")
        if not os.path.exists("token.json") and len(self.stock_names_temp) > 0:
            self.save_stock_list()
            
        self.root.destroy()
        self.exit_event.set()


if __name__ == "__main__":
    controller = Controller()
