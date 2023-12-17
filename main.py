import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import os.path
import pickle

import datetime
import schedule
import time

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
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)

        self.loading_label = tk.Label(
            self, text="I'm still searching, hang on", font=("Roboto", 12)
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

        self.frame_height = 650
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
        self.text_widget = tk.Text(self, wrap=tk.WORD, width=70, height=40)
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.text_widget.place(relx=0.5, rely=0.5, anchor="center")

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
                self.add_centered_text(f"Dividend Google: {stock.dividend_google} \n")

            if stock.dividend_invest10 != None:
                self.add_centered_text(
                    f"Dividend Invest10: {stock.dividend_invest10}\n"
                )

            if stock.price_to_earnings != None:
                self.add_centered_text(
                    f"Price to Earnings: R$ {stock.price_to_earnings}\n"
                )

            if stock.price_to_book != None:
                self.add_centered_text(f"Price to Book: R$ {stock.price_to_book}\n")

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
            self.add_centered_text(f"Price to Book: R$ {stock.price_to_book}\n")
            self.add_centered_text(f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_price_to_earnings(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Results from {last_result.date_of_search}\n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Stock Name: {stock.name}\n")
            self.add_centered_text(f"Price to Earnings: R$ {stock.price_to_earnings}\n")
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
        
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)
        
        # Insert buttons as window widgets in the Text widget

        for i in range(len(self.controller.search_results)):
            button = ttk.Button(
                self.text_widget,
                text=f"{self.controller.search_results[i].date_of_search}",
                command=lambda i=i: self.button_clicked(
                    self.controller.search_results[i]
                ),
            )
            self.text_widget.window_create(tk.END, window=button)
            # Add a newline after each button
            self.text_widget.insert(tk.END, "\n")

            # Center the entire line containing the button
            line_start = f"{i + 1}.0"
            self.text_widget.tag_add(f"button_{i+1}", line_start, f"{line_start}+2l")
            self.text_widget.tag_configure(f"button_{i+1}", justify="center")

        self.text_widget.config(state="disabled")

        self.after(1, self.center_window)

    def button_clicked(self, search_result):
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

        self.frame_height = 650
        self.frame_width = 600
        x_cordinate = int((self.screen_width / 2) - (self.frame_width / 2))
        y_cordinate = int((self.screen_height / 2) - (self.frame_height / 2))
        self.geometry(
            "{}x{}+{}+{}".format(
                self.frame_width, self.frame_height, x_cordinate, y_cordinate
            )
        )
        self.title("Search Data")

        self.main_frame = tk.Frame(self, width=600, height=650, bg="#1D1D20").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        self.button_01 = tk.Button(
            self,
            text="Search From Google",
            width=20,
            bg="#90EE90",
            activebackground="#90EE90",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_dividends_from_google,
        )
        self.button_01.pack(side="left", padx=(95, 0))

        self.button_02 = tk.Button(
            self,
            text="Search From Invest10",
            width=20,
            bg="#089A4F",
            activebackground="#089A4F",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_dividends_from_invest10,
        )
        self.button_02.pack(side="left", padx=(50, 50))


class mainView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.configure(bg="#1D1D20")

        self.root_height = 800
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
            text="Welcome to \nStock Dividends Retriever App",
            bg="#1D1D20",
            font=("Roboto", 20, "bold"),
            fg="#2BABE2",
        )
        self.label.pack(side="top", pady=20)

        self.mainFrame = tk.Frame(self.root, width=900, height=200, bg="#1D1D20").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        self.logo = tk.PhotoImage(file="./img/logo.ppm")

        self.root.wm_iconphoto(False, self.logo)

        self.guide_frame = tk.Frame(self.mainFrame, bg="#1D1D20")
        self.guide_frame.pack()

        self.guide_title = tk.Label(
            self.guide_frame,
            text="Guide",
            bg="#1D1D20",
            font=("Roboto", 15, "bold"),
            fg="#FF3333",
        )
        self.guide_title.pack(side="top", padx=90)

        self.guide_text = tk.Label(
            self.guide_frame,
            text="Here in the app you can make these actions:\n\n"
            "1- Search Dividends\t\t\n"
            "2- Save Dividends\t\t\t\n"
            "3- Generate Excel Table of Dividends\n"
            "4- Get the last dividends search\t",
            bg="#1D1D20",
            font=("Roboto", 13, "bold"),
            fg="white",
        )
        self.guide_text.pack(side="left")
        
        self.label = tk.Label(
            text="Welcome to \nStock Dividends Retriever App",
            bg="#1D1D20",
            font=("Roboto", 20, "bold"),
            fg="#2BABE2",
        )
        self.label.pack(side="top", pady=20)

        self.limg = tk.Label(self.guide_frame, image=self.logo, bg="#1D1D20")
        self.limg.pack()

        self.buttons_frame = tk.Frame(self.mainFrame, bg="#1D1D20")
        self.buttons_frame.pack(pady=(50, 0))

        self.search_button = tk.Button(
            self.buttons_frame,
            text="Search Dividends",
            width=20,
            bg="#90EE90",
            activebackground="#90EE90",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_view,
        )
        self.search_button.pack(side="left", padx=(95, 0))

        self.search_price_to_earnings_button = tk.Button(
            self.buttons_frame,
            text="Search price to Earnings",
            width=20,
            bg="#089A4F",
            activebackground="#089A4F",
            font=("Roboto", 11, "bold"),
            command=controller.search_prices_to_earnings,
        )
        self.search_price_to_earnings_button.pack(side="left", padx=(50, 50))

        self.search_price_to_book_button = tk.Button(
            self.buttons_frame,
            text="Search price to Book",
            width=20,
            bg="#08FF08",
            activebackground="#08FF08",
            font=("Roboto", 11, "bold"),
            command=controller.search_price_to_book,
        )
        self.search_price_to_book_button.pack(side="right", padx=(0, 40))
        self.frame_02 = tk.Frame(self.mainFrame, width=900, height=200, bg="#1D1D20")
        self.frame_02.pack(pady=(50, 0))

        self.stock_search_button = tk.Button(
            self.frame_02,
            text="Search a Stock",
            width=20,
            bg="#0091F7",
            activebackground="yellow",
            font=("Roboto", 11, "bold"),
            command=controller.search_a_stock,
        )
        self.stock_search_button.pack(side="left", padx=(50, 40))


        self.search_all_data_button = tk.Button(
            self.frame_02,
            text="Search All Data",
            width=20,
            bg="yellow",
            activebackground="yellow",
            font=("Roboto", 11, "bold"),
            command=controller.search_all_data_from_all_stocks,
        )
        self.search_all_data_button.pack()

        self.last_search_button = tk.Button(
            self.root,
            text="Search Results",
            width=20,
            bg="yellow",
            activebackground="yellow",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_results_view,
        )
        self.last_search_button.pack(padx=(50, 0), pady=(30, 0))

        self.generate_button = tk.Button(
            self.root,
            text="Generate Excel file",
            width=20,
            bg="yellow",
            activebackground="yellow",
            font=("Roboto", 11, "bold"),
            command=controller.generate_excel_table,
        )
        self.generate_button.pack(padx=(50, 0), pady=(30, 0))
        
        self.save_data_sheets_button = tk.Button(
            self.root,
            text="Save All Data On Sheets",
            width=20,
            bg="#fdf0d5",
            activebackground="#fdf0d5",
            font=("Roboto", 11, "bold"),
            command=self.controller.save_all_data_on_sheets,
        )

        self.save_data_sheets_button.pack(padx=(50, 0), pady=(30, 0))

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
        self.root.title("Stock Dividends Retriever App")

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

        # instances of Stock, used to store the stocks that has other attributes
        self.temporary_stocks = []

        self.dividends_google_list = []
        self.dividends_invest10_list = []
        self.prices_to_book_list = []
        self.price_to_earnings_list = []

        self.stock_names_temp = []

        self.all_data_list = []

        self.temporary_potential_stocks = []

        # Event to signal the thread to exit
        self.exit_event = threading.Event()
        self.loading_event = threading.Event()

        self.already_check_stock_prices = False

        # # Periodically check for the exit condition in the main thread
        self.root.after(0, self.repeating_function)
        self.check_exit_condition()

        self.root.mainloop()

    def repeating_function(self):
        print("Checking time to search stock's new prices!")
        if (
            (datetime.now().minute) % 10 == 0
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

    def save_search_results(self):
        if len(self.search_results) != 0:
            with open("results.pickle", "wb") as f:
                pickle.dump(self.search_results, f)

    def save_potential_stocks_to_buy(self):
        if len(self.potential_stocks_to_buy) != 0:
            with open("potential-stocks-to-buy.pickle", "wb") as f:
                pickle.dump(self.potential_stocks_to_buy, f)

    def show_last_result(self):
        if len(self.search_results) == 0:
            messagebox.showinfo(
                "Empty List",
                "You need to search for at least one time to get the last results!",
            )
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
        func.generate_excel_file(stock_names, dividends_google_list, dividends_invest10_list, prices_to_book_list, price_to_earnings_list)

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
        self.all_data_list = self.get_all_data_from_all_stocks(self.stock_names_temp)

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
            # self.search_results.append(SearchResult(self.temporary_stocks))
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_all_data(self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no dividends !")

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
            success = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno(
                    "Input",
                    "There is no token.json file, but you can still search for a stock. Do you want to continue?",
                    parent=self.root,
                )
                if answer == True:
                    
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == "stop":
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

                    else:
                        search_last_stocks = messagebox.askyesno(
                            "Input",
                            "There is a temporary list of stocks, do you want to search by that?",
                            parent=self.root,
                        )

                        if search_last_stocks == True:
                            # it is used to empty the stocks that has other attributes
                            self.show_loading_bar()
                            threading.Thread(target=self.search_all_data_thread).start()
                            self.root.after(100, self.check_completion)

                        else:
                            self.stock_names_temp = []
                            while True:
                                stock_name = simpledialog.askstring(
                                    "Input",
                                    "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                    parent=self.root,
                                )

                                if stock_name == "stop":
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

        if answer == "" or answer == None:
            messagebox.showerror("Error", "You need to input a stock name!")
            return
        self.show_loading_bar()

        # Start a new thread for stock search
        threading.Thread(target=self.search_a_stock_thread, args=(answer,)).start()

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
            self.show_results_view.show_price_to_earnings(self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_prices_to_earnings(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search prices to earnings ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno(
                    "Input",
                    "There is no token.json file, but you can still search for a stock. Do you want to continue?",
                    parent=self.root,
                )
                if answer == True:
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == "stop":
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

                                if stock_name == "stop":
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
        self.prices_to_book_list = self.get_prices_to_book_data(self.stock_names_temp)

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
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_price_to_book(self):
        self.temporary_stocks = []

        result = messagebox.askquestion(
            "Form", "Are you sure you want to search prices to book ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno(
                    "Input",
                    "There is no token.json file, but you can still search for a stock. Do you want to continue?",
                    parent=self.root,
                )
                if answer == True:
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == "stop":
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

                                if stock_name == "stop":
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
            self.show_results_view.show_invest10_dividends(self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no dividends !")

        self.hide_loading_bar()

    def search_dividends_from_invest10(self):
        self.temporary_stocks = []
        self.choose_search_data_view.destroy()
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search dividends ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno(
                    "Input",
                    "There is no token.json file, but you can still search for a stock. Do you want to continue?",
                    parent=self.root,
                )
                if answer == True:
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == "stop":
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

                                if stock_name == "stop":
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
        result = messagebox.askquestion(
            "Form", "Are you sure you want to search dividends ?"
        )

        if result == "yes":
            self.show_loading_bar()

            if os.path.exists("token.json"):
                self.stock_names_temp = []

            # it will append the stocks thats why it starts empty
            success = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")
            if not success:
                self.hide_loading_bar()
                answer = messagebox.askyesno(
                    "Input",
                    "There is no token.json file, but you can still search for a stock. Do you want to continue?",
                    parent=self.root,
                )
                if answer == True:
                    if len(self.stock_names_temp) == 0:
                        while True:
                            stock_name = simpledialog.askstring(
                                "Input",
                                "What's the name of the stock you want to search?\n If you don't wanna add more stocks just type 'stop'",
                                parent=self.root,
                            )

                            if stock_name == "stop":
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

                                if stock_name == "stop":
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
            messagebox.showinfo("Success", "Dividends Registered Successfully ")

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
            messagebox.showinfo("Success", "Dividends Registered Successfully ")

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
            messagebox.showinfo("Success", "Dividends Registered Successfully ")

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
            messagebox.showinfo("Success", "Dividends Registered Successfully ")

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
            messagebox.showinfo("Success", "Dividends Registered Successfully ")

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
            self.generate_excel_file(self.stock_names_temp, self.all_data_list[0],self.all_data_list[1],self.all_data_list[2],self.all_data_list[3])
            messagebox.showinfo("Success", "The file was created on your downloads !")
            return
        
        elif len(self.dividends_google_list) != 0 and len(self.dividends_invest10_list) != 0 and len(self.prices_to_book_list) != 0 and len(self.price_to_earnings_list) != 0:
            self.generate_excel_file(self.stock_names_temp, self.dividends_google_list,self.dividends_invest10_list,self.prices_to_book_list,self.price_to_earnings_list)
            messagebox.showinfo("Success", "The file was created on your downloads !")
            return
        
        else:
            messagebox.showerror("Error", "There is no sufficient data to generate a excel file!")
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
                post_success = self.post_data_list(self.dividends_google_list, "AA")
                
            if self.dividends_invest10_list:
                post_success = self.post_data_list(self.dividends_invest10_list, "AB")
                
            if self.prices_to_book_list:
                post_success = self.post_data_list(self.prices_to_book_list, "Z")
            
            if self.price_to_earnings_list:
                post_success = self.post_data_list(self.price_to_earnings_list, "Y")
                
            if post_success:
                messagebox.showinfo("Success", "All Data was registered Successfully ")
                
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
        # Price to Earnings
        # Price to Book

        post_success = self.post_data_list(self.all_data_list[0], "AA")
        post_success = self.post_data_list(self.all_data_list[1], "AB")
        post_success = self.post_data_list(self.all_data_list[2], "Z")
        post_success = self.post_data_list(self.all_data_list[3], "Y")

        if post_success:
            messagebox.showinfo("Success", "All Data was registered Successfully ")

        else:
            messagebox.showerror("Error", "Failed to save all Data!")

    def check_exit_condition(self):
        # Periodically check for the exit condition in the main thread
        if not self.exit_event.is_set():
            # Check every second
            self.root.after(1000, self.check_exit_condition)

    def exit_window(self):
        print("exit")
        self.root.destroy()
        self.exit_event.set()


if __name__ == "__main__":
    controller = Controller()
