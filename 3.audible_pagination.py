from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium import *
web ='https://www.audible.in/adblbestsellers?ref=a_hp_t1_navTop_pl1cg0c1r0&pf_rd_p=4e150d5e-ca98-47fb-823b-f6fcb252aced&pf_rd_r=5ZNPZJB39ET4E6GHZZ1S&pageLoadId=4l3aH0gjemHWJBG0&creativeId=2e6787a2-0cd0-4a6e-afe0-05766cd505e5'
path = 'C:/Users/user/Downloads/chromedriver.exe'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
    
   
driver.get(web)
driver.maximize_window()

# Pagination 1
pagination = driver.find_element(by='xpath',value='//ul[contains(@class, "pagingElements")]')  # locating pagination bar
pages = pagination.find_elements(by='tag name',value='li')  # locating each page displayed in the pagination bar
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

book_title = []
book_writer = []
book_length = []
book_narrator=[]
book_releasedate=[]
book_language=[]
book_rating=[]
# Pagination 2
current_page = 1   # this is the page the bot starts scraping

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(2)  # let the page render correctly
    container = driver.find_element(by='class name', value='adbl-impression-container ')
    products = container.find_elements(by='xpath', value='.//li[contains(@class, "productListItem")]')

    for product in products:       
        book_title.append(product.find_element(by='xpath', value='.//h3[contains(@class, "bc-heading")]').text)
        book_writer.append(product.find_element(by='xpath', value='.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(by='xpath', value='.//li[contains(@class, "runtimeLabel")]').text)
        book_narrator.append(product.find_element(by='xpath', value='..//li[contains(@class, "narratorLabel")]').text)
        book_releasedate.append(product.find_element(by='xpath', value='.//li[contains(@class, "releaseDateLabel")]').text)
        book_rating.append(product.find_element(by='xpath', value='.//li[contains(@class, "ratingsLabel")]').text)
        book_language.append(product.find_element(by='xpath', value='.//li[contains(@class, "languageLabel")]').text)
        

    current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
    try:
        next_page = driver.find_element(by='xpath',value='.//span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'Title': book_title, 'Writer': book_writer, 'Narrator': book_narrator, 'Length':book_length , 'Release Date': book_releasedate, 'Language': book_language , 'Ratings':book_rating})
df_books.to_csv('Audible_books_pagination.csv', index=False)
