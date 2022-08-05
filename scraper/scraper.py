from ast import AugAssign
from datetime import date
import requests
import time
import soupsieve
import tabulate
import pandas as pd
import sqlalchemy
import logging
import random

#SQL SETUP ---------------
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy import MetaData

database_username = 'adil'
database_password = 'Huntington13!'
database_url = 'ec2-13-215-51-104.ap-southeast-1.compute.amazonaws.com'
database_name = 'analyst_ln_connections'

database_connection = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(database_username, database_password, database_url, database_name)).connect()

metadata = sqlalchemy.MetaData()

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

LN_HOMEPAGE_URL = 'https://www.linkedin.com/'
LOCATIONS = ['India']

logging.basicConfig(filename="scraper.log", level=logging.DEBUG, format='%(asctime)s - %(message)', datefmt='%d-%b-%y %H:%M:%S')

today = date.today()

df_analyst_list = pd.read_sql_table("analysts", con=database_connection, columns=['id', 'name', 'ln_id'])
print(df_analyst_list)

analyst_list = df_analyst_list.to_dict('records')
print(analyst_list)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("detach", True)
    chrome_path = "/Users/adil/Dropbox/Work Documents/Tanglin VP/Automations/LN Scraper/chromedriver"
    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    params = dict({
        "latitude": 1.464470,
        "longitude": 103.813908,
        "accuracy": 100
    })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
    return driver

def get_page_login(driver):
    driver.get(LN_HOMEPAGE_URL)
    username = driver.find_element(By.ID, "session_key")
    password = driver.find_element(By.ID, "session_password")
    login_button = driver.find_element(By.CLASS_NAME,
                                       "sign-in-form__submit-button")

    time.sleep(random.randint(1,4))

    username.send_keys("adil_do@hotmail.com")
    password.send_keys("Huntington13!")
    login_button.click()

    time.sleep(random.randint(10,15))

    driver.maximize_window()

    for analyst in analyst_list:
      driver.get(f"https://www.linkedin.com/search/results/people/?connectionOf={analyst['ln_id']}&network=%5B%22F%22%2C%22S%22%5D")
      
      time.sleep(random.randint(8,12))

      #hide chat bar
      message_bar = driver.find_element(By.CLASS_NAME, 'msg-overlay-bubble-header')
      message_bar.click()
      driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")      
      
      #find number of pages
      def find_last_page_number():
        page_source = driver.page_source
        global last_page_count
        initial_soup = BeautifulSoup(page_source, 'html.parser')
        pages_array = initial_soup.find_all('li', class_='artdeco-pagination__indicator--number')
        last_page_count = int(pages_array[-1].find('span').text)
        print(last_page_count)
        print(type(last_page_count))
      
      def find_last_page_number_inner():
        page_source = driver.page_source
        global last_page_count_inner
        initial_soup = BeautifulSoup(page_source, 'html.parser')
        try:
          pages_array = initial_soup.find_all('li', class_='artdeco-pagination__indicator--number')
          last_page_count_inner = int(pages_array[-1].find('span').text)
        except:
          print("Only has 1 page")
          last_page_count_inner = 1

      global list_analyst_working
      global dict_analyst_working
      list_analyst_working = []
      dict_analyst_working = {}



      #filter page for location 
      def filter_location(location):

        button_location = driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Locations filter')]")
        button_location.click()
        form_location = driver.find_element(By.XPATH, "//input[@placeholder='Add a location']")
        form_location.send_keys(location)
        time.sleep(random.randint(2,5))
        dropdown_suggestion_location = driver.find_element(By.XPATH, "//div[@id='hoverable-outlet-locations-filter-value']//div[@class='basic-typeahead__triggered-content ']/div/div[1]")
        dropdown_suggestion_location.click()
        time.sleep(random.randint(2,5))
        button_submit_location = driver.find_element(By.XPATH, "//div[@id='hoverable-outlet-locations-filter-value']//button[@aria-label='Apply current filter to show results']")
        button_submit_location.click()

      
      def filter_location_reset():
        button_location = driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Locations filter')]")
        button_location.click()
        time.sleep(random.randint(2,5))
        button_reset_location = driver.find_element(By.XPATH,  "//div[@id='hoverable-outlet-locations-filter-value']//button[@aria-label='Reset selected Locations']")
        button_reset_location.click()
        time.sleep(random.randint(2,5))
        button_submit_location = driver.find_element(By.XPATH, "//div[@id='hoverable-outlet-locations-filter-value']//button[@aria-label='Apply current filter to show results']")
        button_submit_location.click()
        time.sleep(random.randint(2,5))


      #extraction function
      def extract_page():
        page_source = driver.page_source
        
        only_results_div = SoupStrainer('div', class_='search-results-container')
        soup = BeautifulSoup(page_source, 'html.parser', parse_only=only_results_div)
        
        try:
          larger_set = soup.find_all('div', class_='entity-result__content')
        except:
          print("No results")
        else:
          for small_set in larger_set:
            connection_name = small_set.select('[dir="ltr"] > span')[0].text
            try:
              connection_title = small_set.find('div', class_='entity-result__primary-subtitle').text
            except AttributeError:
              print("No title provided")
              connection_title = ""

            try:  
              connection_country = small_set.find('div', class_='entity-result__secondary-subtitle').text
              
            except AttributeError:
              print("No country provided")
              connection_country = ""

            dict_analyst_working['name'] = connection_name
            dict_analyst_working['company'] = connection_title
            dict_analyst_working['country'] = connection_country

            temp_copy = dict_analyst_working.copy()

            list_analyst_working.append(temp_copy)

            dict_analyst_working.pop('name')
            dict_analyst_working.pop('company')
            dict_analyst_working.pop('country')


          print(list_analyst_working)
      
      time.sleep(random.randint(8,13))
      
      #find the last page of analyst's network
      find_last_page_number()

      #check if have more than 100 pages
      if last_page_count == 100:
        #if have more than 100 or more pages, click filter button to cycle through each location
        for location in LOCATIONS:
          print(f"Filtering {analyst['name']}'s connections based in {location}")
          filter_location(location)
          time.sleep(random.randint(2,6))
          #find last page of connection list after specific filtered locaiton
          driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
          time.sleep(random.randint(2,6))
          find_last_page_number_inner()
          #extract through its pages via 'while' loop
          i = 1
          while i <= last_page_count_inner:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(random.randint(3,8))
            extract_page()
            print('page extracted')
            time.sleep(random.randint(3,8))
            #when reach last page break to resume location loop
            if i == 2 or i == last_page_count_inner:
              time.sleep(random.randint(1,4))
              break
            else:
              next_button = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
            time.sleep(random.randint(1,4))
            next_button.click()
            i += 1
          #reset locatio filter before next  
          filter_location_reset()

        #after looping through all locations, insert working list into pandas dataframe  
        df_working=pd.DataFrame(list_analyst_working)
        df_working.drop_duplicates(keep='first')
        print(df_working)
        df_existing = pd.read_sql("SELECT connections.name FROM connections INNER JOIN analysts ON analysts.id = connections.connected_to WHERE analysts.id = %s", params={analyst['id']}, con=database_connection)
        print(df_existing)
        df_pending = pd.concat([df_existing, df_working], ignore_index=True).drop_duplicates(['name'],keep=False)
        print(df_pending)
        df_new = df_pending[~df_pending['name'].isin(df_existing['name'])]
        
        df_new['connection_date'] = today.strftime("%y-%m-%d")
        df_new['connected_to'] = analyst['id']
        
        print('this is the final df_new')
        print(df_new)
        print('adding df_new to sql')
        df_new.to_sql('connections', con=database_connection, if_exists='append', index=False)

        print('attempting to update last updated date')

        analyst_table = sqlalchemy.Table('analysts', metadata, autoload = True, autoload_with=database_connection)
        query = sqlalchemy.update(analyst_table).values(last_updated_date = today.strftime("%y-%m-%d")).where(analyst_table.columns.id == analyst['id'])
        database_connection.execute(query)

        time.sleep(random.randint(1,4))
        
      else:
        i = 1
        while i <= last_page_count:
          print(f"Extracting Page {i} of {analyst['name']}'s connections")
          time.sleep(random.randint(3,7))
          driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
          time.sleep(random.randint(3,7))
          extract_page()
          print('page extracted')
          time.sleep(random.randint(3,7))
          if i == 2:
            df_working=pd.DataFrame(list_analyst_working)
            print(df_working)
            df_existing = pd.read_sql("SELECT connections.name as 'Name' FROM connections INNER JOIN analysts ON analysts.id = connections.connected_to WHERE analyst.id = %s", params={analyst['id']}, con=database_connection)
            
            print(df_existing)
            df_pending = pd.concat([df_existing, df_working], ignore_index=True).drop_duplicates(['name'],keep=False)

            print(df_pending)
            df_new = df_pending[~df_pending['name'].isin(df_existing['name'])]

            #add connected_on and connected_to colums to pandas

            df_new['connection_date'] = today.strftime("%y-%m-%d")
            df_new['connected_to'] = analyst['id']

            

            print(df_new)

            df_new.to_sql('connections', con=database_connection, if_exists='append', index=False)
            
            print('attempting to update last updated date')
            analyst_table = sqlalchemy.Table('analysts', metadata, autoload = True, autoload_with=database_connection)
            query = sqlalchemy.update(analyst_table).values(last_updated_date = today.strftime("%y-%m-%d")).where(analyst_table.columns.id == analyst['id'])
            database_connection.execute(query)

            time.sleep(random.randint(1,4))
            break
          else:
            next_button = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
          time.sleep(random.randint(1,4))
          next_button.click()
          
          i += 1

if __name__ == "__main__":
    print('Creating Driver')
    driver = get_driver()

    print('Logging in')
    login = get_page_login(driver)




    