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


COLUMN_GET_DATA = "Página1!P3:P"

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1limODVbEf9Tpa2fu_YcJ0T7vzfG1E6Ukmw00InzwaUw"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def generate_exel_file(list1, list2, output_file='dividends.xlsx'):
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

def get_dividends(list_names):
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
            
            if '%' not in dividend:
              print(f"falha ao buscar dividendo da {name}")
              dividends.append("0%")
              continue
            
            dividend_float = float(dividend.replace("%","").replace(",","."))
            
            
        except:
            print(f"falha ao buscar dividendo da {name}")
            dividends.append("0%")
            continue
          


            
        print(f'Dividendo da ação {name}: {dividend}')

        dividends.append(dividend)
        
    driver.quit()
    return dividends

def get_stock_names(list_names):
# If modifying these scopes, delete the file token.json.
  



  
  creds = None

  if os.path.exists("token.json"):
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


def get_last_row(service, spreadsheet_id, column_letter):
    # Helper function to get the last row with data in a specific column

    range_name = f"Página1!{column_letter}1:{column_letter}"
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
  




def post_diviends(list_dividends):
    if not list_dividends:
        return False

    formated_list_dividends = [[dividend] for dividend in list_dividends]

    last_row = str(len(list_dividends) + 3)  # 2 for the space between the header and the first row and 1 to return the average
    SAMPLE_RANGE_NAME = f"Página1!Q3:Q" + last_row

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
        range_name = f"Página1!Q3:Q{last_row}"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        values = result.get("values", [])

        if values:

            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Página1!Q{int(last_row) + 1}",
                                  valueInputOption="USER_ENTERED", body={"values": [[f'=TEXT(AVERAGE(Q3:Q{int(last_row) -1});"0.00%")']]}).execute()

            # Insert an empty row after the average
            # sheet.batchUpdate(
            #     spreadsheetId=SAMPLE_SPREADSHEET_ID,
            #     body={
            #         "requests": [
            #             {
            #                 "insertDimension": {
            #                     "range": {
            #                         "sheetId": 0,
            #                         "dimension": "ROWS",
            #                         "startIndex": int(last_row) -1,
            #                         "endIndex": int(last_row) 
            #                     },
            #                     "inheritFromBefore": False
            #                 }
            #             }
            #         ]
            #     }
            # ).execute()

    except HttpError as err:
        print(err)
        return False

    return True
    
    



if __name__ == "__main__":
    
    stock_symbols = [
        "BMGB4","KLBN4","CMIN3","USIM5","MRFG3","TAEE4","BRSR6","AURE3","SANB4","VBBR3","GGBR3","TRPL4"]

# Print the list
    print(stock_symbols)

    # list_names = get_stock_names()
    # print(list_names)
    list_dividends = get_dividends(stock_symbols)
    print(list_dividends)
    if post_diviends(list_dividends):
        print("Dividendos registrados com sucesso feito com sucesso!")
  
  
  