# How to Use?

- Make sure the chrome driver is in the same location as the script.
- Run the py file `scrapper.py`
- When prompted enter the following
   - Search term preferably `Samsung mobile or Apple mobiles`
   - Expected number of products in the result. For default enter `0` default value is 10. Max value is 72.
  - Provide a value in between `0-4` to sort the product listing on the webpage. Sort by relevance is set to default.
     > * 0 = Low to High
     > * 1 = High to Low
     > * 2 = Relevance
     > * 3 = Popularity
     > * 4 = Newest First
- Excel Sheet will be created and stored in the same location as script.
- please turn on `wrap text` in excel to have a better look at the details captured.

## Libraries Used
```python
import re #regx to format text
from openpyxl import Workbook # r/w excel file
import time #to introduce delay
from selenium import webdriver #browser
from selenium.webdriver.common.by import By #by class to use XPATH
```
## Problems Solved
#### PROBLEM 1

> Accepting search term, as user input. Tested with terms Samsung mobiles, Apple mobiles.

> Generates an excel file containing Product Name, Storage, User Rating & Price.

#### PROBLEM 2

> Accepting the number of products to be written in an excel file from the user. Max results can be obtained is 72 (3 Pages)

> Users can sort by the following options. Only one can be chosen at the time because Flipkart supports only one at a time.

> Unlike Amazon, in Flipkart Pincode can be entered only on buying page, since it wasn’t possible to show that part in the script, it will be jotted down here:
```python
driver.find_element(By.XPATH, "//input[contains(@class, '_36yFo0')]").send_keys(“400072”) #this will copy the pin code in the text box  
driver.find_element(By.XPATH, "//span[contains(@class, '_2P_LDn')]").click() #click the check button
```
The location of the particular input and buttons are searched by using `XPATH`.

#### PROBLEM 3

> To keep the entire process like human behavior delay and time gaps are introduced in the required part of the code like clicking the search button, navigating pages for more results, and so on. 