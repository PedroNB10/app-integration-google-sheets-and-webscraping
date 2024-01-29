import os.path
import pandas as pd
# libraries to get and update google sheets
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# libraries to get the dividends:
from selenium import webdriver
from selenium.webdriver.common.by import By

from pathlib import Path
from dotenv import load_dotenv  # pip install python-dotenv
import ast
import json

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)


SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")


if not os.path.exists("token.json"):
    data = os.getenv("MY_TOKEN")
    print(data)
    print(type(data))
    data = json.loads(data)
    with open("token.json", 'w') as json_file:
        json.dump(data, json_file)






SHEET_NAME = "Página1"
DY_COLUMN_UPDATE_GOOGLE = "AF"

# COLUMN FROM WHERE TO GET THE DATA FROM THE GOOGLE SHEET
COLUMN_GET_DATA = f"{SHEET_NAME}!A3:A"



# The ID and range of a sample spreadsheet.

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]




def get_all_data_from_all_stocks(stock_list):

    list_all_data = []
    list_google_dividends = []
    list_invest10_dividends = []
    list_price_to_earnings = []
    list_price_to_book = []
    list_roe = []
    list_net_margin = []
    real_time_prices = []
    list_payout = []
    list_net_debts = []
    list_cagr = []
    
    
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    # getting data from investidor10
    for stock in stock_list:
                
        # getting the didivend yield from invest10
        url = f'https://investidor10.com.br/acoes/{stock}/'
        driver.get(url)
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'DY')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            dividend_yield = other_parent_element.text
            
            if '%' not in dividend_yield:
              print(f"Failed to find the dividend from {stock}")
              dividend_yield = "--"
            
            
            print(f'Invest10 Dividend from {stock}: {dividend_yield}')
        except:
            print(f"Failed to find the dividend from {stock}")
            dividend_yield = "--"
            print(f'Invest10 Dividend from {stock}: {dividend_yield}')
            
        list_invest10_dividends.append(dividend_yield)
        
        
        # getting the price per profit
        url = f'https://investidor10.com.br/acoes/{stock}/'
    
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/L')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price = other_parent_element.text
            
        except:
            print(f"Failed to get the Price to Earnings from {stock}")
            price = "--"
        print(f'Price to earnings from {stock}: {price}')
        list_price_to_earnings.append(price)
            
        # getting the price per value
        url = f'https://investidor10.com.br/acoes/{stock}/'
    
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price = other_parent_element.text
            
        except:
            print(f"Failed to get the Price to Book from {stock}")
            price = "--"
        print(f"Price to Book from: {stock}: {price}")    
        list_price_to_book.append(price)
        
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'ROE')]").find_element(By.XPATH, "..")
        
            
            other_parent_element = element.find_element(By.XPATH,".//div[1]")
            span = other_parent_element.find_element(By.XPATH,".//span")
            roe = span.text
            
            
            if '%' not in roe:
              print(f"Failed to find the ROE from {stock}")
              roe = "--"
              
            
        except:
            print(f"Failed to get the ROE from {stock}")
            roe = "--"
        print(f'ROE from {stock}: {roe}')    
        list_roe.append(roe)
        
        try:
            
                element = driver.find_element(By.XPATH, "//span[contains(text(), 'MARGEM LÍQUIDA')]").find_element(By.XPATH, "..")
            
                
                other_parent_element = element.find_element(By.XPATH,".//div[1]")
                span = other_parent_element.find_element(By.XPATH,".//span")
                net_margin = span.text
    
                if '%' not in net_margin:
                    print(f"Failed to find the Net Margin from {stock}")
                    net_margin = "--"
              
                
        except:
                print(f"Failed to get the Net Margin from {stock}")
                net_margin = "--"
                
        print(f'Net Margin from {stock}: {net_margin}')        
        list_net_margin.append(net_margin)
                
        
        try:
            
                element = driver.find_element(By.XPATH, "//span[contains(text(), 'DÍVIDA LÍQUIDA / EBITDA')]").find_element(By.XPATH, "..")
            
                
                other_parent_element = element.find_element(By.XPATH,".//div[1]")
                span = other_parent_element.find_element(By.XPATH,".//span")
                net_debt = span.text
                

              
                
        except:
                print(f"Failed to get the DÍVIDA LÍQUIDA / EBITDA  from {stock}")
                net_debt = "--"
        print(f'Net Debt from {stock}: {net_debt}')        
        list_net_debts.append(net_debt)
        
        
        try:
            
                element = driver.find_element(By.XPATH, "//span[contains(text(), 'CAGR RECEITAS 5 ANOS')]").find_element(By.XPATH, "..")
            
                
                other_parent_element = element.find_element(By.XPATH,".//div[1]")
                span = other_parent_element.find_element(By.XPATH,".//span")
                cagr = span.text
            
                
        except:
                print(f"Failed to get the CAGR RECEITAS 5 ANOS  from {stock}")
                cagr = "--"
        print(f'CAGR RECEITAS 5 ANOS: from {stock}: {cagr}')        
        list_cagr.append(cagr)
        
        try:
            
                element = driver.find_element(By.XPATH, "//span[contains(text(), 'PAYOUT')]").find_element(By.XPATH, "..")
            
                
                other_parent_element = element.find_element(By.XPATH,".//div[1]")
                span = other_parent_element.find_element(By.XPATH,".//span")
                payout = span.text
                
                if '%' not in payout:
                    print(f"Failed to find the PAYOUT from {stock}")
                    payout = "--"
              
                
        except:
                print(f"Failed to get the PAYOUT from {stock}")
                payout = "--"
        print(f'PAYOUT from {stock}: {payout}')        
        list_payout.append(payout)
        
        
        
                   
        print("\n")
    
    # getting data from google
    for stock in stock_list:
         # getting the dividend
        url = f'https://www.google.com/search?q=dividendos+{stock}'
        driver.get(url)
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), '%')]")

            dividend = element.text
            if '%' not in dividend:
              print(f"Failed to find the dividend from {stock}")
              dividend = "--"
            
            if len(dividend) > 6:
                dividend = "--"    
            
            
            
        except:
            print(f"Failed to find the dividend from {stock}")
            dividend = "--"
            
        print(f'Google Dividend from {stock}: {dividend}')
        list_google_dividends.append(dividend)
        
        try:
            if dividend != "--":
                element_list = driver.find_elements(By.XPATH, "//span[contains(text(), 'BRL')]")
                if len(element_list) > 1:
                    element = element_list[1]
             
                    
                parent_element = element.find_element(By.XPATH, "..")
                
                price = parent_element.text
                price_float = "R$ " + (price.replace("BRL",""))
            else:
                url = f'https://www.google.com/search?q={stock}'
                driver.get(url)


                element = driver.find_element(By.XPATH, "//span[contains(text(), 'BRL')]")
                parent_element = element.find_element(By.XPATH, "..")
                
                price = parent_element.text
                price_float = "R$ " + (price.replace("BRL",""))
            
            
                
            

        except:
            print(f"Failed to find the price from {stock}")
            price = "R$ 0,00"
        print(f'Google Real Time Price from {stock}: {price_float}')    
        real_time_prices.append(price_float)
    
    list_all_data.append(list_google_dividends)
    list_all_data.append(list_invest10_dividends)
    list_all_data.append(list_price_to_earnings)
    list_all_data.append(list_price_to_book)
    list_all_data.append(list_roe)
    list_all_data.append(list_net_margin)
    list_all_data.append(real_time_prices)
    list_all_data.append(list_net_debts)
    list_all_data.append(list_payout)
    list_all_data.append(list_cagr)
    
    driver.quit()     
    return list_all_data



def get_data_from_a_stock(stock_symbol):
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    list_data = []
    
    # getting the dividend
    url = f'https://www.google.com/search?q=dividendos+{stock_symbol}'
    driver.get(url)
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), '%')]")

        dividend = element.text
        
    except:
        print(f"Failed to find the dividend from {stock_symbol}")
        dividend = "--"
    print(f'Google Dividend from {stock_symbol}: {dividend}')    
    list_data.append(dividend)
    
    try:
        if dividend != "--":
            element_list = driver.find_elements(By.XPATH, "//span[contains(text(), 'BRL')]")
            if len(element_list) > 1:
                element = element_list[1]
         
                
            parent_element = element.find_element(By.XPATH, "..")
            
            price = parent_element.text
            price_float = "R$ " + (price.replace("BRL",""))
        else:
            url = f'https://www.google.com/search?q={stock_symbol}'
            driver.get(url)


            element = driver.find_element(By.XPATH, "//span[contains(text(), 'BRL')]")
            parent_element = element.find_element(By.XPATH, "..")
            
            price = parent_element.text
            price_float = "R$ " + (price.replace("BRL",""))
            
            
    except:
        print(f"Failed to find the price from {stock_symbol}")
        price = "--"
    
    print(f'Google Real Time Price from {stock_symbol}: {price_float}')
    list_data.append(price_float)
    
    
    
    
    # getting the didivend yield from invest10
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
    driver.get(url)
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'DY')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        dividend_yield = other_parent_element.text
        
    except:
        print(f"Failed to find the dividend from {stock_symbol}")
        dividend_yield = "--"
    print(f'Invest10 Dividend from {stock_symbol}: {dividend_yield}')    
    list_data.append(dividend_yield)
    
    
    # getting the price per profit
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/L')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        price = other_parent_element.text
        
    except:
        print(f"Failed to get the Price to Earnings from {stock_symbol}")
        price = "--"
    print(f'Price to earnings from {stock_symbol}: {price}')    
    list_data.append(price)
        
    # getting the price per value
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
   
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        price = other_parent_element.text
        print(f"Price to Book from: {stock_symbol}: {price}")
    except:
        print(f"Failed to get the Price to Book from {stock_symbol}")
        price = "--"
        
    list_data.append(price)
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'ROE')]").find_element(By.XPATH, "..")
    
        
        other_parent_element = element.find_element(By.XPATH,".//div[1]")
        span = other_parent_element.find_element(By.XPATH,".//span")
        roe = span.text
        
        
    
    except:
        print(f"Failed to get the ROE from {stock_symbol}")
        roe = "--"
        
    list_data.append(roe)
    print(f'ROE from {stock_symbol}: {roe}')
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'MARGEM LÍQUIDA')]").find_element(By.XPATH, "..")
        
        
        other_parent_element = element.find_element(By.XPATH,".//div[1]")
        span = other_parent_element.find_element(By.XPATH,".//span")
        net_margin = span.text
        
        
    except:
        print(f"Failed to get the Net Margin from {stock_symbol}")
        net_margin = "--"
    print(f'Net Margin from {stock_symbol}: {net_margin}')
    list_data.append(net_margin)
    
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'DÍVIDA LÍQUIDA / EBITDA')]").find_element(By.XPATH, "..")
        
        
        other_parent_element = element.find_element(By.XPATH,".//div[1]")
        span = other_parent_element.find_element(By.XPATH,".//span")
        net_debt = span.text
        
    except:
        print(f"Failed to get the DÍVIDA LÍQUIDA / EBITDA  from {stock_symbol}")
        net_debt = "--"
        
    list_data.append(net_debt)
    print(f'Net Debt from {stock_symbol}: {net_debt}')
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'CAGR RECEITAS 5 ANOS')]").find_element(By.XPATH, "..")
        
        
        other_parent_element = element.find_element(By.XPATH,".//div[1]")
        span = other_parent_element.find_element(By.XPATH,".//span")
        cagr = span.text
        
    
    except:
        print(f"Failed to get the CAGR RECEITAS 5 ANOS  from {stock_symbol}")
        cagr = "--"
        
    list_data.append(cagr)
    print(f'CAGR RECEITAS 5 ANOS: from {stock_symbol}: {cagr}')
    
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'PAYOUT')]").find_element(By.XPATH, "..")
        
        
        other_parent_element = element.find_element(By.XPATH,".//div[1]")
        span = other_parent_element.find_element(By.XPATH,".//span")
        payout = span.text
        
    except:
        print(f"Failed to get the PAYOUT from {stock_symbol}")
        payout = "--"
        
    list_data.append(payout)
    print(f'PAYOUT from {stock_symbol}: {payout}')
        
        

    driver.quit()
    
    return list_data


def get_colum_data_from_sheets(list_names, COLUMN_GET_DATA):
    creds = None

    if os.path.exists("token.json"): #  verify if the token.json file exists, if not, return the error to the user
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        return False

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=COLUMN_GET_DATA)
            .execute()
        )
        
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return


        # Print columns A and E, which correspond to indices 0 and 4.
        for value in values:
            list_names.append(value[0])
        

        
        
        return True
    
    except HttpError as err:
        print(err)
        return False
    

def generate_excel_file(list1, list2, list3, list4, list5, output_file='stockinfo.xlsx'):
    # Check if the lists have the same length
    if len(list1) != len(list2) != len(list3) != len(list4) != len(list5):
        raise ValueError("All five lists must have the same length.")

    # Create a DataFrame from the lists
    data = {'Stock': list1, 'Google Dividend': list2, 'Invest10 Dividend': list3, 'Price to Book': list4, 'Price to Earnings': list5}
    df = pd.DataFrame(data)

    # Get the path to the "Downloads" directory
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Set the full path for the output file in the "Downloads" directory
    output_path = os.path.join(downloads_dir, output_file)
    df.to_excel(output_path, index=False)
    print(f"Excel file '{output_path}' created successfully.")  
    

def get_roes_from_invest10(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    roes = []
    driver.maximize_window()
    
    for  name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)
    
        try:
        
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'ROE')]").find_element(By.XPATH, "..")
        
            
            other_parent_element = element.find_element(By.XPATH,".//div[1]")
            span = other_parent_element.find_element(By.XPATH,".//span")
            roe = span.text
            if '%' not in roe:
                print(f"Failed to find the ROE from {name}")
                roe = "0%"
            roes.append(roe)
            
            
            print(f'ROE from {name}: {roe}')
        except:
            print(f"Failed to get the ROE from {name}")
            roes.append("0%")
            continue
               
    driver.quit()

    return roes


def get_net_margins(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    net_margins = []
    driver.maximize_window()
    
    for name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)
    
        try:
        
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'MARGEM LÍQUIDA')]").find_element(By.XPATH, "..")
        
            
            other_parent_element = element.find_element(By.XPATH,".//div[1]")
            span = other_parent_element.find_element(By.XPATH,".//span")
            net_margin = span.text
            if '%' not in net_margin:
                print(f"Failed to find the Net Margin from {name}")
                net_margin = "0%"
                
            net_margins.append(net_margin)
            
            
            print(f'Net Margin from {name}: {net_margin}')
        except:
            print(f"Failed to get the Net Margin from {name}")
            net_margin.append("0%")
            continue
               
    driver.quit()

    return net_margins


def get_price_to_book_from_invest10(list_names):
    if (list_names == []):
      return list_names
  
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    prices = []
    driver.maximize_window()

    for  name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)
        
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price = other_parent_element.text
            prices.append(price)
            
        except:
            print(f"Failed to get the Price to Book from {name}")
            prices.append("0")
            continue
               
    driver.quit()

    return prices

def get_price_to_earnings(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    prices = []
    driver.maximize_window()
    for  name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/L')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price = other_parent_element.text

        except:
            print(f"Failed to get the Price to Earnings from {name}")
            prices.append("0")
            continue
          
        print(f'Price to earnings from {name}: {price}')

        prices.append(price)
        
    driver.quit()
    return prices

  
def get_price_to_book(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    prices = []
    driver.maximize_window()
    for  name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price = other_parent_element.text

            
            
        except:
            print(f"Failed to get the Price to Book from {name}")
            prices.append("0")
            continue
          
        print(f"Price to Book from: {name}: {price}")

        prices.append(price)
        
    driver.quit()
    return prices
    
def get_dividends_from_invest10(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    dividends = []
    driver.maximize_window()
    for  name in list_names:
        url = f'https://investidor10.com.br/acoes/{name}/'
        driver.get(url)

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'DY')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            dividend = other_parent_element.text
            dividend_float = float(dividend.replace("%","").replace(",","."))
            
            
        except:
            if '%' not in dividend:
              print(f"Failed to find the dividend from {name}")
              dividends.append("0%")
              continue
          
            dividends.append("0%")
            continue
          
        print(f'Invest10 Dividend from {name}: {dividend}')

        dividends.append(dividend)
        
    driver.quit()
    print("%" in dividends)
    return dividends

def get_dividends_google_data(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    dividends = []
    driver.maximize_window()
    for  name in list_names:
        url = f'https://www.google.com/search?q=dividendos+{name}'
        driver.get(url)

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), '%')]")
            dividend = element.text
            dividend_float = float(dividend.replace("%","").replace(",","."))
            
            
        except:
            if '%' not in dividend:
              print(f"Failed to find the dividend from {name}")
              dividends.append("0%")
              continue
          
            dividends.append("0%")
            continue
          
        print(f'Google Dividend from {name}: {dividend}')

        dividends.append(dividend)
        
    driver.quit()
    return dividends

def get_real_time_prices(list_names):
    if (list_names == []):
      return list_names
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    prices = []
    driver.maximize_window()
    for  name in list_names:
        url = f'https://www.google.com/search?q={name}'
        driver.get(url)

        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'BRL')]")
            parent_element = element.find_element(By.XPATH, "..")
            
            price = parent_element.text
            price_float = "R$ " + (price.replace("BRL",""))
            
            
        except:
            print(f"Failed to find the price from {name}")
            prices.append("0")
            continue
          
        print(f'Google Real Time Price from {name}: {price}')

        prices.append(price_float)
        
    driver.quit()
    return prices

def get_stock_names(list_names):
  creds = None

  if os.path.exists("token.json"): #  verify if the token.json file exists, if not, return the error to the user
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  else:
    return False

  with open("token.json", "w") as token:
    token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=COLUMN_GET_DATA)
        .execute()
    )
    
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    print(values)
      # Print columns A and E, which correspond to indices 0 and 4.
    for value in values:
      print(f"{value[0]}")
      list_names.append(value[0])
    
    return True
  
    
      
  except HttpError as err:
    print(err)
    return False





def get_last_row(service, spreadsheet_id, column_letter):
    # Helper function to get the last row with data in a specific column

    range_name = f"{SHEET_NAME}!{column_letter}1:{column_letter}"
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )

    values = result.get("values", [])

    if not values:
        return None

    last_row = len(values)
    return last_row
  

def update_stock_names_columns_google_sheets(list_names, update_column_letter):
    if not list_names:
      return False

    formated_list_stocks = [[dividend] for dividend in list_names]
    print(f"tamanho da lista: {len(list_names)}")
    last_row = str(len(list_names) +  2) 
    SAMPLE_RANGE_NAME = f"{SHEET_NAME}!{update_column_letter}3:{update_column_letter}" + last_row

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Update the dividends
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                       valueInputOption="USER_ENTERED", body={"values": formated_list_stocks}).execute()





    except HttpError as err:
        print(err)
        return False

    return True


def add_empty_column_google_sheets(sheet, last_row):
    # Insert an empty row after the average
            sheet.batchUpdate(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                body={
                    "requests": [
                        {
                            "insertDimension": {
                                "range": {
                                    "sheetId": 0,
                                    "dimension": "ROWS",
                                    "startIndex": int(last_row) -1,
                                    "endIndex": int(last_row) 
                                },
                                "inheritFromBefore": False
                            }
                        }
                    ]
                }
            ).execute()

def post_data_list(list_dividends, DY_COLUMN_UPDATE_GOOGLE):
    if not list_dividends:
        return False

    formated_list_dividends = [[dividend] for dividend in list_dividends]

    last_row = str(len(list_dividends) + 3)  # 2 for the space between the header and the first row and 1 to return the average
    SAMPLE_RANGE_NAME = f"{SHEET_NAME}!{DY_COLUMN_UPDATE_GOOGLE}3:{DY_COLUMN_UPDATE_GOOGLE}" + last_row

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Update the dividends
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                       valueInputOption="USER_ENTERED", body={"values": formated_list_dividends}).execute()

        # Calculate the average and update the last value
        # range_name = f"{SHEET_NAME}!{DY_COLUMN_UPDATE_GOOGLE}3:{DY_COLUMN_UPDATE_GOOGLE}{last_row}"
        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        # values = result.get("values", [])

        # if values:

        #     sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"{SHEET_NAME}!{DY_COLUMN_UPDATE_GOOGLE}{int(last_row) + 1}",
        #                           valueInputOption="USER_ENTERED", body={"values": [[f'=ARRED(AVERAGE({DY_COLUMN_UPDATE_GOOGLE}3:{DY_COLUMN_UPDATE_GOOGLE}{int(last_row) -1}); 2)']]}).execute()

            
    

    except HttpError as err:
        print(err)
        return False

    return True
    
    



if __name__ == "__main__":
    stock_symbols = ["BMGB4","KLBN4", "SLAEUMANO", "VALE3"]
    print(get_data_from_a_stock(stock_symbols[0]))


  
  
  