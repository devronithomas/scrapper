#gocomet-Web Crawler Assignment

#imports
import re #regx to format text
from openpyxl import Workbook # r/w excel file
import time
from selenium import webdriver #browser
from selenium.webdriver.common.by import By #by class to use XPATH

#user inputs
search_name = "samsung mobile"
results = input('''Press Enter for Default
Number of products (>10): ''')

try:
    if results == "":
        results = 10
except:
    if results < 10:
        results = 10
    elif results > 73:
        print ("out of range")
        quit()
    else:
        pass

#filters
sort = int(input('''Press Enter for Default
Sort Price or Relevance By:
0 = Low to High
1 = High to Low
2 = Relevance
3 = Popularity
4 = Newest First
'''))
def sort_by_price_relevance(sort=2): #filters
    if sort == 0:
        driver.find_element_by_xpath("//div[contains(@class, '_10UF8M') and text()='Price -- Low to High']").click() #click low to high
    elif sort == 1:
        driver.find_element_by_xpath("//div[contains(@class, '_10UF8M') and text()='Price -- High to Low']").click() #click high to low
    elif sort == 2:
        driver.find_element_by_xpath("//div[contains(@class, '_10UF8M') and text()='Relevance']").click() #click relevance
    elif sort == 3:
        driver.find_element_by_xpath("//div[contains(@class, '_10UF8M') and text()='Popularity']").click() #click popularity
    elif sort == 4:
        driver.find_element_by_xpath("//div[contains(@class, '_10UF8M') and text()='Newest First']").click() #click newest first

print("Getting results")

#creating a web driver
driver_path="C:\\Users\\ronit\\Desktop\\Python\\Apps\\gocomet\\chromedriver.exe"
driver=webdriver.Chrome(executable_path=driver_path)

#search in browser
driver.get("https://www.flipkart.com/")
driver.implicitly_wait(10) #wait for popup

#to close the login popup
try:
    driver.find_element(By.XPATH, "//button[contains(@class, '_2KpZ6l _2doB4z')]").click()
except:
    pass


driver.implicitly_wait(10) #wait before adding the search term

driver.find_element(By.XPATH, "//input[contains(@class, '_3704LK')]").send_keys(search_name) #adding search term in search box
driver.find_element(By.XPATH, "//button[contains(@class, 'L0Z3Pu')]").click() #click search button

#creating list to store phone, variant, price
phones, storage, ratings, prices_flipkart = [], [], [], []

#looping to populate the list
def populate():
    sort_by_price_relevance(sort)
    time.sleep(1)
    phones_fk = driver.find_elements(By.XPATH, "//div[contains(@class, '_4rR01T')] | //div[contains(@class, 's1Q9rs')]")#creating list of all avilable phones
    prices_fk = driver.find_elements(By.XPATH, "//div[contains(@class, '_30jeq3 _1_WHN1')] | //div[contains(@class, '_30jeq3')]")#creating list of prices
    user_rating = driver.find_elements(By.XPATH, "//div[contains(@class, '_3LWZlK')]")#Ratings

    for phone,price,rating in zip(phones_fk, prices_fk, user_rating):
        phone_name= re.sub(r"[\(\[].*?[\)\]]","", phone.text)#formating phone name
        phones.append(phone_name) #adding name to list

        if "GB" in phone.text: #checking if variant
            variant = re.findall(r"\w+\sGB\b",phone.text) #extracting Variant
            storage.append(variant[0])#gives a list so indexing the first element
            # print (variant[0])
        else:
            storage.append("N/A")
            # print("N/A")
        prices_flipkart.append(price.text) #appending price to list
        ratings.append(rating.text)
        # print (phone_name, price.text)

if results < 25:
    print ("Capturing Page 1")
    populate() #calls populate function
elif results < 49:
    print ("Capturing Page 1")
    populate()
    print ("Capturing Page 2")
    driver.find_element_by_link_text("2").click() #click on page 2
    driver.implicitly_wait(10)
    time.sleep(1) #delay
    populate()
elif results < 73:
    print ("Capturing Page 1")
    populate()
    print ("Capturing Page 2")
    driver.find_element_by_link_text("2").click() #click on page 2
    driver.implicitly_wait(10)
    time.sleep(1)
    populate()
    print ("Capturing Page 3")
    driver.find_element_by_link_text("3").click() #click on page 3
    driver.implicitly_wait(10)
    time.sleep(1)
    populate()

#combining retrived info
details = zip(phones[:results], storage[:results+1], ratings[:results+1], prices_flipkart[:results+1]) #retreving only required results

#looping above list
# for data in list(details): #converting zip object to list
#     print (data)

#writing everything to excel file
wb = Workbook()
sh = wb.active

print ("Populating Excel")

sh.append(["Name", "Storage", "Rating", "Price"])
for data in list(details): #converting zip object to list
    sh.append(data)

wb.save(search_name + ".xlsx") #saving excel file

#-------------Compairing with amazon-------------

# tab_switch = 1

# for phone, variant in zip(phones, storage):
#     driver.implicitly_wait(10)
#     driver.get("https://www.amazon.in/")#open amazon website
#     driver.implicitly_wait(5)
#     driver.find_element(By.XPATH, "//input[contains(@id, 'searchtextbox')]").send_keys(phone)#search for phone name
#     driver.find_element(By.XPATH, "//input[contains(@id, 'nav-search-submit-button')]").click()#click search button
#     driver.implicitly_wait(5)
#     driver.find_element(By.XPATH, "//span[contains(@class, 'a-size-medium a-color-base a-text-normal')]").click()#click on the first result
#     driver.switch_to.window(driver.window_handles[tab_switch])#switch to active tab
#     driver.implicitly_wait(5)
#     try:
#         price_amazon=driver.find_element(By.XPATH,"//span[contains(@id, 'priceblock_dealprice')] | //span[contains(@id, 'priceblock_ourprice')] ")#scrape the price
#         price_amazon=price_amazon.text
#     except:
#         price_amazon = "Not Available"

#     print (price_amazon) #print price
#     prices_amazon.append(price_amazon.text) #append to list
#     tab_switch += 1 #inc tab

# driver.quit()#quit browser
print ("Process Finished")