from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import sys

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver')
 
driver.get('https://www.google.com/maps/place/University+of+Waterloo/@43.4595444,-80.5470463,17z/data=!4m7!3m6!1s0x882bf6ad02edccff:0xdd9df23996268e17!8m2!3d43.4722854!4d-80.5448576!9m1!1b1')


## Step 1: Google Review Pane


htmlSource = driver.page_source


print(htmlSource)

