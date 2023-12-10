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


SHEET_NAME = "Página1"
DY_COLUMN_UPDATE_GOOGLE = "AF"

# COLUMN FROM WHERE TO GET THE DATA FROM THE GOOGLE SHEET
COLUMN_GET_DATA = f"{SHEET_NAME}!A3:A"



# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1fIzQZevwQ9UB6ynmRNvGddYf9ITDEuhp5lgM34-VDNs"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]




def get_all_data_from_all_stocks(stock_list):

    list_all_data = []
    list_google_dividends = []
    list_invest10_dividends = []
    list_price_to_earnings = []
    list_price_to_book = []
    
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    for stock in stock_list:
        
    

        # getting the dividend
        url = f'https://www.google.com/search?q=dividendos+{stock}'
        driver.get(url)
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), '%')]")

            dividend = element.text
            if '%' not in dividend:
              print(f"Failed to find the dividend from {stock}")
              dividend = "0%"
            
            if len(dividend) > 6:
                dividend = "0%"    
            
            
            print(f'Google Dividend from {stock}: {dividend}')
        except:
            print(f"Failed to find the dividend from {stock}")
            dividend = "0%"
            print(f'Google Dividend from {stock}: {dividend}')
        list_google_dividends.append(dividend)
        
        
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
              dividend_yield = "0%"
            
            
            print(f'Invest10 Dividend from {stock}: {dividend_yield}')
        except:
            print(f"Failed to find the dividend from {stock}")
            dividend_yield = "0%"
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
            print(f'Price to earnings from {stock}: {price}')
        except:
            print(f"Failed to get the Price to Earnings from {stock}")
            price = "0"
            
        list_price_to_earnings.append(price)
            
        # getting the price per value
        url = f'https://investidor10.com.br/acoes/{stock}/'
    
        try:
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
            parent_element = element.find_element(By.XPATH, "..")
            grand_parent_element = parent_element.find_element(By.XPATH, "..")
            other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
            price_vp = other_parent_element.text
            print(f"Price to Book from: {stock}: {price_vp}")
        except:
            print(f"Failed to get the Price to Book from {stock}")
            price_vp = "0"
            
            
            
        list_price_to_book.append(price_vp)
        print("\n")
  
    
    list_all_data.append(list_google_dividends)
    list_all_data.append(list_invest10_dividends)
    list_all_data.append(list_price_to_earnings)
    list_all_data.append(list_price_to_book)
    
    
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
        print(f'Dividendo da ação {stock_symbol}: {dividend}')
    except:
        print(f"falha ao buscar dividendo da {stock_symbol}")
        dividend = "0%"
        
    list_data.append(dividend)
    
    
    # getting the didivend yield from invest10
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
    driver.get(url)
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'DY')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        dividend_yield = other_parent_element.text
        print(f'Dividend Yield da ação {stock_symbol}: {dividend_yield}')
    except:
        print(f"falha ao buscar Dividend Yield da {stock_symbol}")
        dividend_yield = "0%"
        
    list_data.append(dividend_yield)
    
    
    # getting the price per profit
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
 
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/L')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        price = other_parent_element.text
        print(f'P/L da ação {stock_symbol}: {price}')
    except:
        print(f"falha ao buscar P/L da {stock_symbol}")
        price = "0"
        
    list_data.append(price)
        
    # getting the price per value
    url = f'https://investidor10.com.br/acoes/{stock_symbol}/'
   
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        price_vp = other_parent_element.text
        print(f'P/VP da ação {stock_symbol}: {price_vp}')
    except:
        print(f"falha ao buscar P/VP da {stock_symbol}")
        price_vp = "0"
        
    list_data.append(price_vp)
        

    driver.quit()
    
    return list_data
    


def generate_excel_file(list1, list2, output_file='dividends.xlsx'):
   # Check if the lists have the same length
    if len(list1) != len(list2):
        raise ValueError("The two lists must have the same length.")

    # Create a DataFrame from the lists
    data = {'stock': list1, 'dividends': list2}
    df = pd.DataFrame(data)

    # Get the path to the "Downloads" directory
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Set the full path for the output file in the "Downloads" directory
    output_path = os.path.join(downloads_dir, output_file)
    df.to_excel(output_path, index=False)
    print(f"Excel file '{output_path}' created successfully.")  
    

# def get_price_to_earnings(list_names):
#     if (list_names == []):
#       return list_names
  
  
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(options=options)
#     prices = []
#     driver.maximize_window()

#     for  name in list_names:
#         url = f'https://investidor10.com.br/acoes/{name}/'
#         driver.get(url)
        
      
#         element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/L')]").find_element(By.XPATH, "..")
#         parent_element = element.find_element(By.XPATH, "..")
#         grand_parent_element = parent_element.find_element(By.XPATH, "..")
#         other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
#         price = other_parent_element.text
#         prices.append(price)
               
#     driver.quit()
#     return prices


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
        
      
        element = driver.find_element(By.XPATH, "//span[contains(text(), 'P/VP')]").find_element(By.XPATH, "..")
        parent_element = element.find_element(By.XPATH, "..")
        grand_parent_element = parent_element.find_element(By.XPATH, "..")
        other_parent_element = grand_parent_element.find_element(By.XPATH,".//div[2]")
        price = other_parent_element.text
        prices.append(price)
               
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
            prices.append("0")
            continue
          
        print(f'Preço P/L da ação {name}: {price}')

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
            prices.append("0")
            continue
          
        print(f'Preço P/VP da ação {name}: {price}')

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
              print(f"falha ao buscar dividendo da {name}")
              dividends.append("0%")
              continue
          
            dividends.append("0%")
            continue
          
        print(f'Dividendo da ação {name}: {dividend}')

        dividends.append(dividend)
        
    driver.quit()
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
              print(f"falha ao buscar dividendo da {name}")
              dividends.append("0%")
              continue
          
            dividends.append("0%")
            continue
          
        print(f'Dividendo da ação {name}: {dividend}')

        dividends.append(dividend)
        
    driver.quit()
    return dividends

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
      
    # update_stock_names_columns_google_sheets(list_names, "T")
    # update_stock_names_columns_google_sheets(list_names, "R")
    # update_stock_names_columns_google_sheets(list_names, "W")
    # update_stock_names_columns_google_sheets(list_names, "AC")
    
    
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

def post_dividends_google_data(list_dividends):
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
        range_name = f"{SHEET_NAME}!{DY_COLUMN_UPDATE_GOOGLE}3:{DY_COLUMN_UPDATE_GOOGLE}{last_row}"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        values = result.get("values", [])

        if values:

            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"{SHEET_NAME}!{DY_COLUMN_UPDATE_GOOGLE}{int(last_row) + 1}",
                                  valueInputOption="USER_ENTERED", body={"values": [[f'=TEXT(AVERAGE({DY_COLUMN_UPDATE_GOOGLE}3:{DY_COLUMN_UPDATE_GOOGLE}{int(last_row) -1});"0.00%")']]}).execute()

            
    

    except HttpError as err:
        print(err)
        return False

    return True
    
    



if __name__ == "__main__":
    
    stock_symbols = ["BMGB4","KLBN4","CMIN3","USIM5","MRFG3","TAEE4","BRSR6","AURE3","SANB4","VBBR3","GGBR3","TRPL4"]

    # lista=get_price_to_book_from_invest10(stock_symbols)
    print(get_all_data_from_all_stocks(stock_symbols))

    # print(lista)
# # Print the list
#     print(stock_symbols)
    # list_names = []
    # get_stock_names(list_names)
    # print(list_names)
    # list_dividends = get_dividends(stock_symbols)
    # print(list_dividends)
    # if post_diviends(list_dividends):
    #     print("Dividendos registrados com sucesso feito com sucesso!")
  
  
  