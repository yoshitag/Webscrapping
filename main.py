from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

options = Options()
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), chrome_options=options)

# open the webpage
driver.get('https://www.rottentomatoes.com/browse/movies_in_theaters')

while True:
    try:
        # scroll to the bottom of the page
        _ = driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # locate the Load More Button
        load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='discovery__actions']/button")))
        # Click the button
        load_more_button.click()
    except:
        break

# locate all the movie elements
movies_elements = driver.find_elements(by = By.XPATH, value = "//a[@class='js-tile-link ']")
len(movies_elements)


movies_list = [x.get_attribute('href') for x in movies_elements]
len(movies_list)
print(movies_list[0])

# getting all the movie info from each movie
smaller_list = movies_list[:5]    # creating a smaller subset of list to test out the code
row_list = list()   # initiating a row list where each element is one row of our future df

for each_movie in smaller_list:
    # open the movie page
    driver.get(each_movie)
    # locate and extract the movie synopsis text blob
    movieSynopsis = driver.find_element(by=By.XPATH, value="//p[@data-qa='movie-info-synopsis']").text
    # grab the movieinfo box
    movieInfo = driver.find_elements(by=By.XPATH,value="//ul[@id='info']/li")
    row_dict = dict()   # initiating a row dict to store all the column- value pairs of each row
    for each_info in movieInfo:
        field = each_info.text
        k, v = field.split(': ')
        row_dict[k] = v
    row_dict['movie_id'] = each_movie
    row_dict['synopsis'] = movieSynopsis
    row_list.append(row_dict)

# create a pandas df from the scraped data
import pandas as pd
df = pd.DataFrame(row_list)
df.head(3).T





