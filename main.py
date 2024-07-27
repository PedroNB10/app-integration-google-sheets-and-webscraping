import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import os.path
import pickle

import datetime
from datetime import datetime


from models import Stock, SearchResult, PotentialStockToBuy
from pages import LoadingView, ShowResultsView, ShowUserGuideView,  ChooseSearchDataView, SearchResultsView


import functions as func
import send_email as sd


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
            text="Seja Bem-Vindo ao \n Rastreador de Ações ",
            bg="#1c1830",
            height=0,
            font=("Roboto", 17, "bold"),
            fg="#2BABE2",

        )
        self.label.pack(side="top", pady=20)

        self.logo = tk.PhotoImage(file="./img/logo-new.ppm")

        self.root.wm_iconphoto(False, self.logo)

        self.guide_button = tk.Button(
            text="Guia de Uso",
            width=20,
            bg="#C62068",
            fg="white",
            cursor="hand2",
            activebackground="#C62068",
            font=("Roboto", 11, "bold"),
            command=controller.show_user_guide,

        ).place(relx=0.8, rely=0.1, anchor="center")

        self.search_button = tk.Button(

            text="Pesquisar Dividendos",
            width=20,
            bg="#1c1830",
            fg="white",
            cursor="hand2",
            activebackground="#1c1830",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_view,
        ).place(relx=0.2, rely=0.25, anchor="center")

        self.search_price_to_earnings_button = tk.Button(
            text="Pesquisar P / L",
            width=20,
            bg="#14182C",
            fg="white",
            cursor="hand2",
            activebackground="#14182C",
            font=("Roboto", 11, "bold"),
            command=controller.search_prices_to_earnings,
        ).place(relx=0.5, rely=0.25, anchor="center")

        self.search_price_to_book_button = tk.Button(

            text="Pesquisar P / VP",
            width=20,
            bg="#1c1830",
            fg="white",
            cursor="hand2",
            activebackground="#1c1830",
            font=("Roboto", 11, "bold"),
            command=controller.search_price_to_book,
        ).place(relx=0.8, rely=0.25, anchor="center")

        self.stock_search_button = tk.Button(

            text="Pesquisar uma ação",
            width=20,
            bg="#293B57",
            fg="white",
            cursor="hand2",
            activebackground="#293B57",
            font=("Roboto", 11, "bold"),
            command=controller.search_a_stock,
        ).place(relx=0.35, rely=0.4, anchor="center")

        self.search_all_data_button = tk.Button(

            text="Pesquisar Todos Indicadores",
            width=30,
            bg="#293B57",
            fg="white",
            activebackground="#293B57",
            cursor="hand2",
            font=("Roboto", 11, "bold"),
            command=controller.search_all_data_from_all_stocks,
        ).place(relx=0.65, rely=0.4, anchor="center")

        self.last_search_button = tk.Button(
            text="Resultados das Últimas Pesquisas",
            width=30,
            bg="#456990",
            fg="white",
            cursor="hand2",
            activebackground="#456990",
            font=("Roboto", 11, "bold"),
            command=controller.create_search_results_view,
        ).place(relx=0.5, rely=0.55, anchor="center")

        self.generate_button = tk.Button(
            text="Gerar Uma Tabela Excel",
            width=30,
            bg="#9A2C5D",
            fg="white",
            cursor="hand2",
            activebackground="#9A2C5D",
            font=("Roboto", 11, "bold"),
            command=controller.generate_excel_table,
        ).place(relx=0.5, rely=0.65, anchor="center")

        self.save_data_sheets_button = tk.Button(
            text="Salvar Dados no Google Sheets",
            width=30,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.save_all_data_on_sheets,
        ).place(relx=0.5, rely=0.75, anchor="center")

        self.create_a_stock_list_button = tk.Button(
            text="Criar uma lista de ações",
            width=20,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.create_stock_list,
        ).place(relx=0.20, rely=0.1, anchor="center")

        self.search_roes_button = tk.Button(
            text="Pesquisar ROE",
            width=20,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_roes_from_invest10,
        ).place(relx=0.2, rely=0.65, anchor="center")

        self.search_net_margins_button = tk.Button(
            text="Pesquisar Margem Líquida",
            width=24,
            bg="#b6174b",
            fg="white",
            cursor="hand2",
            activebackground="#b6174b",
            font=("Roboto", 11, "bold"),
            command=self.controller.search_net_margins,
        ).place(relx=0.8, rely=0.65, anchor="center")

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
        self.root.title("Rastreador de Ações")
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
        self.roe_list = []
        self.net_margin_list = []

        self.all_data_list = []

        self.temporary_potential_stocks = []

        # Event to signal the thread to exit
        self.exit_event = threading.Event()
        self.loading_event = threading.Event()

        # # Periodically check for the exit condition in the main thread
        self.root.after(1000, self.repeating_function)
        self.check_exit_condition()

        self.root.mainloop()

    def repeating_function(self):
        print(datetime.now().second)
        if (
            (datetime.now().second) == 0  # every 1 minute
            and not self.exit_event.is_set()
            and not self.loading_event.is_set()
        ):
            self.root.after(0, self.track_daily_prices)
            self.root.after(600000, self.track_daily_prices)

        # checking time every 1 second
        self.root.after(1000, self.repeating_function)

    # only is called in case the user doesnt have a token.json file
    def save_stock_list(self):
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
            "Bem-vindo ao aplicativo Rastreador de Ações!\n\n"
            "Desenvolvido para apoiar investidores em decisões informadas sobre ações, este aplicativo utiliza diversos parâmetros da Bolsa de Valores "
            "para proporcionar insights estratégicos sobre oportunidades de investimento. Usuários acessam informações essenciais por meio de funcionalidades como:\n\n"
            "1. Busca por Rendimento de Dividendos: Obtenha dados de duas fontes distintas - Google e Investidor10.\n"
            "2. Busca por Índice Preço/Lucro: Avalie o valor da ação pelo preço dividido pelos lucros.\n"
            "3. Busca por Índice Preço/Ativos: Avalie a saúde financeira pela relação preço/ativos.\n\n"
            "Além dessas funcionalidades, usuários acompanham o histórico de pesquisas e geram um arquivo Excel com as informações buscadas.\n\n"
            "Outra funcionalidade notável é a integração ao Google Sheets. Com login, atualize e recupere parâmetros em um arquivo na nuvem. "
            "Sem login, crie e armazene sua lista personalizada de ações.\n\n"
            "O aplicativo também oferece análises detalhadas de ações, fornecendo informações valiosas para apoiar decisões de investimento. "
            "Características adicionais incluem:\n\n"
            "1. Visualização Detalhada de Ações:\n"
            "   - Nome da Ação\n"
            "   - Preço Atual\n"
            "   - Preço Alvo\n\n"
            "2. Dividendos:\n"
            "   - Dividendo do Google\n"
            "   - Dividendo do Investidor10\n"
            "   - PAYOUT\n\n"
            "3. Indicadores Financeiros:\n"
            "   - Preço / Lucro\n"
            "   - Preço / Valor Patrimonial\n"
            "   - ROE (Return on Equity)\n"
            "   - Margem Líquida\n"
            "   - Dívida Líquida / EBITDA\n\n"
            "4. Crescimento e Desempenho:\n"
            "   - CAGR LUCROS 5 ANOS\n\n"
            "Essas informações são fundamentais para análises abrangentes das ações, permitindo decisões informadas ao avaliar potencial de retorno "
            "e fundamentos das ações."
        )

        self.show_user_guide_view = ShowUserGuideView(self.root, self)
        self.show_user_guide_view.add_centered_text(user_guide)

    def show_last_result(self):
        if len(self.search_results) == 0:
            messagebox.showinfo(
                "Lista de Resultados Vazia",
                "Você precisa pesquisar pelo menos uma vez para obter os últimos resultados!",
            )
            return

        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data()

    def create_stock_list(self):
        print(self.stock_names_temp)
        if len(self.stock_names_temp) > 0:
            answer = messagebox.askyesno(
                "Lista Existente",
                "Você já possui uma lista de ações, deseja criar uma nova? (Observação: a lista antiga será apagada!)"
            )

            if answer == True:
                self.stock_names_temp = []
                while True:
                    stock = simpledialog.askstring(
                        "Entrada",
                        "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                        parent=self.root,
                    )
                    if stock == None and len(self.stock_names_temp) == 0:
                        return
                    if stock == "stop" and len(self.stock_names_temp) == 0:
                        return

                    if stock == "stop" and len(self.stock_names_temp) > 0:
                        return

                    if (stock == "" or stock == None) and len(self.stock_names_temp) == 0:
                        messagebox.showerror(
                            "Erro", "Você precisa inserir o nome de uma ação!")
                        continue

                    if stock != "stop" and stock != None and stock != "":
                        self.stock_names_temp.append(stock)

        else:
            while True:
                stock = simpledialog.askstring(
                    "Entrada",
                    "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                    parent=self.root,
                )
                if stock == None and len(self.stock_names_temp) == 0:
                    return
                if stock == "stop" and len(self.stock_names_temp) == 0:
                    return

                if stock == "stop" and len(self.stock_names_temp) > 0:
                    return

                if (stock == "" or stock == None) and len(self.stock_names_temp) == 0:
                    messagebox.showerror(
                        "Erro", "Você precisa inserir o nome de uma ação!")
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

    def get_roes_from_invest10(self, stock_names):
        return func.get_roes_from_invest10(stock_names)

    def get_net_margins(self, stock_names):
        return func.get_net_margins(stock_names)

    def get_data_from_a_stock(self, stock_name):
        return func.get_data_from_a_stock(stock_name)

    def get_all_data_from_all_stocks(self, stock_names):
        return func.get_all_data_from_all_stocks(stock_names)

    def get_colum_data_from_sheets(self, list_prices, COLUMN_GET_DATA):
        if func.get_colum_data_from_sheets(list_prices, COLUMN_GET_DATA):
            return True
        else:
            return False
  

    def create_search_view(self):
        self.choose_search_data_view = ChooseSearchDataView(self.root, self)

    def create_search_results_view(self):
        if len(self.search_results) == 0:
            messagebox.showinfo(
                "Lista de Resultados Vazia",
                "Você precisa pesquisar pelo menos uma vez para obter os últimos resultados!",
            )
            return

        self.search_results_view = SearchResultsView(self.root, self)

    def search_all_data_thread(self):
        self.all_data_list = []

        target_prices = []
        success = self.get_colum_data_from_sheets(
            target_prices, "Página1!B3:B")
        if not success:
            print("There is no data in the sheets")

        # print(target_prices)

        # it will append the stocks thats why it starts empty
        self.all_data_list = self.get_all_data_from_all_stocks(
            self.stock_names_temp)

        if len(self.all_data_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):

                    # in this case there is no token.json representing the google sheets to get the target prices
                    if len(target_prices) == 0:
                        for i in range(len(self.stock_names_temp)):
                            target_prices.append(None)

                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            dividend_google=self.all_data_list[0][i],
                            dividend_invest10=self.all_data_list[1][i],
                            price_to_earnings=self.all_data_list[2][i],
                            price_to_book=self.all_data_list[3][i],
                            roe=self.all_data_list[4][i],
                            net_margin=self.all_data_list[5][i],
                            real_time_price=self.all_data_list[6][i],
                            target_price=target_prices[i],
                            net_debt=self.all_data_list[7][i],
                            cagr=self.all_data_list[8][i],
                            payout=self.all_data_list[9][i],

                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_all_data(self.search_results[0])

        else:
            messagebox.showerror("Erro", "Não há dados!")

        self.hide_loading_bar()

    def search_all_data_from_all_stocks(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Formulário", "Você tem certeza que deseja pesquisar todos os indicadores?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
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
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                    "Erro", "Você precisa inserir o nome de uma ação!"
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
                        real_time_price=list_data[1],
                        dividend_invest10=list_data[2],
                        price_to_earnings=list_data[3],
                        price_to_book=list_data[4],
                        roe=list_data[5],
                        net_margin=list_data[6],
                        net_debt=list_data[7],
                        cagr=list_data[8],
                        payout=list_data[9],
                    )
                ]
            ),
        )
        self.show_results_view = ShowResultsView(self.root, self)
        self.show_results_view.show_all_data(self.search_results[0])

    def search_a_stock(self):
        answer = simpledialog.askstring(
            "Entrada",
            "Qual o nome da ação que deseja pesquisar?",
            parent=self.root,
        )

        if answer == None:
            return

        if answer == "":
            messagebox.showerror(
                "Erro", "Você precisa inserir o nome de uma ação!")
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
            messagebox.showerror("Erro", "Não há P / L !")

        self.hide_loading_bar()

    def search_prices_to_earnings(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Formulário", "Você tem certeza que deseja pesquisar o P / L ?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
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
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                    "Erro", "Você precisa inserir o nome de uma ação!"
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
            "Formulário", "Você tem certeza que deseja pesquisar o P / VP ?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
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
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                    "Erro", "Você precisa inserir o nome de uma ação!"
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
            "Formulário", "Você tem certeza que deseja pesquisar os dividendos?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
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
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                    "Erro", "Você precisa inserir o nome de uma ação!"
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
            "Formulário", "Você tem certeza que deseja pesquisar os dividendos?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
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
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
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
                                    "Erro", "Você precisa inserir o nome de uma ação!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_google_dividends_thread).start()
            self.root.after(100, self.check_completion)

    def search_roes_from_invest10(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Formulário", "Você tem certeza que deseja pesquisar os ROEs?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_roe_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_roe_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_roe_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Erro", "Você precisa inserir o nome de uma ação!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_roe_thread).start()
            self.root.after(100, self.check_completion)

    def get_roe_thread(self):
        self.roe_list = []
        self.roe_list = self.get_roes_from_invest10(
            self.stock_names_temp
        )  # it will append the stocks thats why it starts empty

        if len(self.roe_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            roe=self.roe_list[i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_roes(
                self.search_results[0])

        else:
            messagebox.showerror("Error", "There is no roes !")

        self.hide_loading_bar()

    def search_net_margins(self):
        self.temporary_stocks = []
        result = messagebox.askquestion(
            "Formulário", "Você tem certeza que deseja pesquisar as margens líquidas?"
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
                            "Entrada",
                            "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                            parent=self.root,
                        )

                        if stock_name == None and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) == 0:
                            return

                        if stock_name == "stop" and len(self.stock_names_temp) > 0:
                            self.show_loading_bar()
                            threading.Thread(
                                target=self.get_net_margins_thread
                            ).start()
                            self.root.after(100, self.check_completion)
                            break

                        if stock_name == "" or stock_name == None:
                            messagebox.showerror(
                                "Erro", "Você precisa inserir o nome de uma ação!"
                            )
                            continue
                        else:
                            self.stock_names_temp.append(stock_name)

                else:
                    search_last_stocks = messagebox.askyesno(
                        "Entrada",
                        "Há uma lista temporária de ações, você deseja pesquisar por ela?",
                        parent=self.root,
                    )

                    if search_last_stocks == True:
                        self.show_loading_bar()
                        threading.Thread(
                            target=self.get_net_margins_thread
                        ).start()
                        self.root.after(100, self.check_completion)

                    else:
                        self.stock_names_temp = []
                        while True:
                            stock_name = simpledialog.askstring(
                                "Entrada",
                                "Qual o nome da ação que deseja pesquisar?\n Se não quiser adicionar mais ações digite 'stop'",
                                parent=self.root,
                            )

                            if stock_name == None and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) == 0:
                                return

                            if stock_name == "stop" and len(self.stock_names_temp) > 0:
                                self.show_loading_bar()
                                threading.Thread(
                                    target=self.get_net_margins_thread
                                ).start()
                                self.root.after(100, self.check_completion)
                                break

                            if stock_name == "" or stock_name == None:
                                messagebox.showerror(
                                    "Erro", "Você precisa inserir o nome de uma ação!"
                                )
                                continue
                            else:
                                self.stock_names_temp.append(stock_name)

                return

            threading.Thread(target=self.get_net_margins_thread).start()
            self.root.after(100, self.check_completion)

    def get_net_margins_thread(self):
        self.net_margin_list = []
        self.net_margin_list = self.get_net_margins(
            self.stock_names_temp
        )

        if len(self.net_margin_list) > 0:
            if len(self.temporary_stocks) == 0:
                for i in range(len(self.stock_names_temp)):
                    self.temporary_stocks.append(
                        Stock(
                            self.stock_names_temp[i],
                            net_margin=self.net_margin_list[i],
                        )
                    )

            self.search_results.insert(0, SearchResult(self.temporary_stocks))
            self.save_search_results()
            self.show_results_view = ShowResultsView(self.root, self)
            self.show_results_view.show_net_margins(
                self.search_results[0])

        else:
            messagebox.showerror("Erro", "Não há margens líquidas!")

        self.hide_loading_bar()

    def compare_real_time_prices(self):
        print("Comparing real time prices!")
        self.stock_names_temp = []
        # print(self.stock_names_temp)
        got_data = False

        got_data = self.get_colum_data_from_sheets(self.stock_names_temp, "Página1!A3:A")

        if not got_data:
            print("Deu erro para buscar ações")
            error_message = "Dê uma olhada na planilha na coluna -- SYMBOL -- de nomes das ações! Pode ser que você tenha colocado algum valor inválido em alguma célula ou esquecido de preencher algum valor entre duas células, lembre-se de que o programa não entende espaços em branco entre as ações!"
            sd.send_email_alert("Erro ao obter os nomes das ações!",error_message)
            return



        self.target_price_list = []

        got_data = self.get_colum_data_from_sheets(self.target_price_list, "Página1!B3:B")

        if not got_data:
            error_message = "Dê uma olhada na planilha na coluna de -- Preço Alvo -- das ações! Pode ser que você tenha colocado algum valor inválido em alguma célula ou esquecido de preencher algum valor entre duas células, lembre-se de que o programa não entende espaços em branco entre as células preenchidas!"
            sd.send_email_alert("Erro ao obter os preços alvo das ações!",error_message)
            return

        

        last_row = len(self.target_price_list) + 2
        self.real_time_prices_list = []

        got_data = self.get_colum_data_from_sheets(
            self.real_time_prices_list, f"Página1!D3:D{last_row}"
        )

        if not got_data:
            error_message = "Dê uma olhada na planilha na coluna PRICE que se refere ao preço atual das ações! Pode ser que você tenha colocado algum valor inválido em alguma célula ou esquecido de preencher algum valor entre duas células, lembre-se de que o programa não entende espaços em branco entre as células preenchidas!"
            sd.send_email_alert("Erro ao obter os preços reais das ações!",error_message)
            return

        # print(self.real_time_prices_list)
        # print(self.target_price_list)

        for i in range(len(self.real_time_prices_list)):
            try:

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

            except:
                print("Erro ao converter os preços das ações!")
                sd.send_email_alert("Erro ao converter os preços das ações!", "Verifique a coluna -- PRICE -- se os preços estão no formato correto!")
                return

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
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_google_list, "AA")

        if post_success:
            messagebox.showinfo(
                "Successo", "Dividendos Registrados com Sucesso ")

        else:
            messagebox.showerror(
                "Erro", "Dividendos não podem ser registrados antes da pesquisa!"
            )

    def save_dividends_invest10(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_invest10_list, "AB")

        if post_success:
            messagebox.showinfo(
                "Successo", "Dividendos Registrados com Sucesso ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def save_prices_to_book(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        post_success = self.post_data_list(self.prices_to_book_list, "Z")

        if post_success:
            messagebox.showinfo(
                "Successo", "P/VP Registrados com Sucesso ")

        else:
            messagebox.showerror(
                "Erro", "P/VP não pode ser registrado antes da pesquisa!"
            )

    def save_prices_to_earnings(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        post_success = self.post_data_list(self.price_to_earnings_list, "Y")

        if post_success:
            messagebox.showinfo(
                "Successo", "P/L Registrados com Sucesso ")

        else:
            messagebox.showerror(
                "Erro", "P/L não pode ser registrado antes da pesquisa!"
            )

    def save_dividends_google(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        post_success = self.post_data_list(self.dividends_google_list, "AF")

        if post_success:
            messagebox.showinfo(
                "Successo", "Dividendos Registrados com Sucesso ")

        else:
            messagebox.showerror(
                "Error", "Dividends can't be registered before the search!"
            )

    def show_last_results(self):
        if len(self.dividends_google_list) == 0:
            messagebox.showinfo(
                "Lista de Resultados Vazia",
                "Você precisa pesquisar pelo menos uma vez para obter os últimos resultados!",
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
                "Successo", "O arquivo foi criado na sua pasta de downloads !")
            return

        elif len(self.dividends_google_list) != 0 and len(self.dividends_invest10_list) != 0 and len(self.prices_to_book_list) != 0 and len(self.price_to_earnings_list) != 0:
            self.generate_excel_file(self.stock_names_temp, self.dividends_google_list,
                                     self.dividends_invest10_list, self.prices_to_book_list, self.price_to_earnings_list)
            messagebox.showinfo(
                "Successo", "O arquivo foi criado na sua pasta de downloads !")
            return

        else:
            messagebox.showerror(
                "Erro", "Você precisa pesquisar todos os indicadores pelo menos uma vez para gerar a tabela!")
            return

    def save_all_data_on_sheets(self):
        if not os.path.exists("token.json"):
            messagebox.showerror(
                "Erro",
                "Não há o arquivo token.json, você não pode salvar no google sheets!",
            )
            return

        if (len(self.dividends_google_list) > 0 or len(self.dividends_invest10_list) > 0 or len(self.prices_to_book_list) > 0 or len(self.price_to_earnings_list) > 0 or len(self.roe_list) > 0 or len(self.net_margin_list) > 0) and len(self.all_data_list) == 0:

            if self.price_to_earnings_list:
                post_success = self.post_data_list(
                    self.price_to_earnings_list, "Y")

            if self.prices_to_book_list:
                post_success = self.post_data_list(
                    self.prices_to_book_list, "Z")

            if self.dividends_google_list:
                post_success = self.post_data_list(
                    self.dividends_google_list, "AA")

            if self.dividends_invest10_list:
                post_success = self.post_data_list(
                    self.dividends_invest10_list, "AB")

            if self.roe_list:
                post_success = self.post_data_list(
                    self.roe_list, "AC")

            if self.net_margin_list:
                post_success = self.post_data_list(
                    self.net_margin_list, "AD")

            if post_success:
                messagebox.showinfo(
                    "Sucesso", "Os dados foram registrados com sucesso!")

            else:
                messagebox.showerror("Erro", "Falha ao Salvar os Dados!")

            return

        if len(self.all_data_list) == 0:
            messagebox.showinfo(
                "Lista de Resultados Vazia",
                "Você precisa pesquisar pelo menos uma vez para obter os últimos resultados!",
            )
            return

        # Google dividends
        # Invest10 Dividends
        # Share Price / Earnings per Share
        # Share Price / Book Value per Share

        post_success = self.post_data_list(self.all_data_list[0], "AA")
        post_success = self.post_data_list(self.all_data_list[1], "AB")
        post_success = self.post_data_list(self.all_data_list[2], "Y")
        post_success = self.post_data_list(self.all_data_list[3], "Z")
        post_success = self.post_data_list(self.all_data_list[4], "AC")
        post_success = self.post_data_list(self.all_data_list[5], "AD")

        post_success = self.post_data_list(self.all_data_list[7], "AE")
        post_success = self.post_data_list(self.all_data_list[8], "AF")
        post_success = self.post_data_list(self.all_data_list[9], "AG")

        if post_success:
            messagebox.showinfo(
                "Sucesso", "Os dados foram registrados com sucesso!")

        else:
            messagebox.showerror("Erro", "Falha ao Salvar os Dados!")

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
