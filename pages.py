import tkinter as tk
from tkinter import ttk


class LoadingView(tk.Toplevel):
    def __init__(self, root, controller):
        tk.Toplevel.__init__(self, root)
        self.controller = controller
        self.root = root
        self.title("Pesquisando")
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
            self, text="Pesquisando...", font=("Roboto", 12), fg="white", bg="#1c1830"
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
        self.title("Resultados da Pesquisa")
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
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")

            if stock.real_time_price != None:
                self.add_centered_text(
                    f"Preço Atual: {stock.real_time_price}\n")

            if stock.target_price != None:
                self.add_centered_text(
                    f"Preço Alvo: {stock.target_price}\n")

            if stock.dividend_google != None:
                self.add_centered_text(
                    f"Dividendo do Google: {stock.dividend_google}\n")

            if stock.dividend_invest10 != None:
                self.add_centered_text(
                    f"Dividendo do Investidor10: {stock.dividend_invest10}\n"
                )

            if stock.price_to_earnings != None:
                self.add_centered_text(
                    f"Preço / Lucro: {stock.price_to_earnings}\n"
                )

            if stock.price_to_book != None:
                self.add_centered_text(
                    f"Preço / Valor Patrimonial: {stock.price_to_book}\n")

            if stock.roe != None:
                self.add_centered_text(
                    f"ROE: {stock.roe}\n")

            if stock.net_margin != None:
                self.add_centered_text(
                    f"Margem Líquida: {stock.net_margin}\n")

            if stock.net_debt != None:
                self.add_centered_text(
                    f"Dívida Líquida / EBITDA: {stock.net_debt}\n")

            if stock.cagr != None:
                self.add_centered_text(
                    f"CAGR LUCROS 5 ANOS: {stock.cagr}\n")

            if stock.payout != None:
                self.add_centered_text(
                    f"PAYOUT: {stock.payout}\n")

            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_google_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(f"Dividendo do Google: {
                                   stock.dividend_google}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_invest10_dividends(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(f"Dividendo do Investidor10: {
                                   stock.dividend_invest10}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_prices_to_book(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(
                f"Preço / Valor Patrimonial: {stock.price_to_book}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_price_to_earnings(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(
                f"Preço / Lucro: {stock.price_to_earnings}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_roes(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(
                f"ROE: {stock.roe}\n")
            self.add_centered_text(
                f"----------------------------------------\n")

        self.text_widget.config(state="disabled")

    def show_net_margins(self, search_result):
        last_result = search_result
        self.add_centered_text(f"Resultados do dia {
                               last_result.date_of_search.strftime('%d/%m/%Y %H:%M')} \n")
        self.add_centered_text(f"----------------------------------------\n")
        for stock in last_result.stocks:
            self.add_centered_text(f"Nome da Ação: {stock.name}\n")
            self.add_centered_text(
                f"Margem Líquida: {stock.net_margin}\n")
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
        self.title("Guia de Uso")
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
                text=f"{self.controller.search_results[i].date_of_search.strftime(
                    '%d/%m/%Y %H:%M')}",
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
        self.title("Pesquisar Dividendos")
        self.logo = tk.PhotoImage(file="./img/logo.ppm")
        self.wm_iconphoto(False, self.logo)

        self.main_frame = tk.Frame(self, width=600, height=650, bg="#1c1830").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        self.button_01 = tk.Button(
            self,
            text="Pesquisar no Google",
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
            text="Pesquisar no Investidor10",
            width=30,
            cursor="hand2",
            fg="white",
            bg="#9A2C5D",
            activebackground="#9A2C5D",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_dividends_from_invest10,
        )
        self.button_02.pack(side="left", padx=(50, 50))
