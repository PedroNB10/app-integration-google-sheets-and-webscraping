from datetime import datetime


class Stock:
    def __init__(
        self,
        name,
        dividend_google=None,
        dividend_invest10=None,
        price_to_earnings=None,
        price_to_book=None,
        roe=None,
        net_margin=None,
        real_time_price=None,
        target_price=None,
        net_debt=None,
        cagr=None,
        payout=None,
    ):
        self.name = name
        self.dividend_google = dividend_google
        self.dividend_invest10 = dividend_invest10
        self.price_to_earnings = price_to_earnings
        self.price_to_book = price_to_book
        self.roe = roe
        self.net_margin = net_margin
        self.real_time_price = real_time_price
        self.target_price = target_price
        self.net_debt = net_debt
        self.cagr = cagr
        self.payout = payout

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
