from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome( options=options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
browser.get('https://shop.coles.com.au/a/glenorchy/product/schweppes-soft-drink-solo-lemon-375ml-cans')
sleep(5)
browser.get("https://shop.coles.com.au/a/glenorchy/product/schweppes-soft-drink-sunkist-orange-crush-375ml-cans")