import os.path

# libraries to get and update google sheets
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# libraries to get the dividends:
from selenium import webdriver
from selenium.webdriver.common.by import By



def get_dividends(list_names):
    if (list_names == []):
      return []
  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    dividends = []
    driver.maximize_window()
    for  name in list_names:
        
        url = f'https://www.google.com/search?q=dividendos+{name}'

        driver.get(url)

        
        dividend = '0%'
        
        try:
            element = driver.find_element(By.CLASS_NAME, "YhEN7")
            dividend = element.text

        except:
            print(f"falha ao buscar dividendo da {name}")

            
        # print(f'Dividendo da ação {name}: {dividend}')
        dividends.append(dividend)
        
    driver.quit()
    return dividends

def get_stock_names():
# If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
  SAMPLE_SPREADSHEET_ID = "1s1-S5w9shzTjul6Zosl2tNbv0w1fvEb8H0qq7MoFKkk"
  SAMPLE_RANGE_NAME = "Página1!P3:P22"
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          'client_secret.json', SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return


      # Print columns A and E, which correspond to indices 0 and 4.
    list_names = []
    for value in values:
      list_names.append(value[0])
      
    return list_names
      
  except HttpError as err:
    print(err)


def post_diviends(list_dividends):
  if (list_dividends == []):
    return False
    
  formated_list_dividends = []
  
  for dividend in list_dividends:
      new_dividend = []

      new_dividend.append(dividend)
      formated_list_dividends.append(new_dividend)
        
    # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
  SAMPLE_SPREADSHEET_ID = "1s1-S5w9shzTjul6Zosl2tNbv0w1fvEb8H0qq7MoFKkk"
  SAMPLE_RANGE_NAME = "Página1!Q3:Q22"
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          'client_secret.json', SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED",
                body={"values":formated_list_dividends}).execute()
    )
    

  except HttpError as err:
    print(err)
    return False

  return True
    



if __name__ == "__main__":

    list_names = get_stock_names()
    print(list_names)
    list_dividends = get_dividends(list_names)
    print(list_dividends)
    if post_diviends(list_dividends):
        print("Dividendos registrados com sucesso feito com sucesso!")
  
  
  