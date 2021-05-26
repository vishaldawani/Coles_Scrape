

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait as wait

from bs4 import BeautifulSoup as soup
from time import sleep
import time
import pandas as pd
import requests
import sys
import utils
import random
import numpy as np
import config
import ProductScrapeFuncs as PSF
import chardet
import cProfile
import snakeviz

# DECLARE GLOBAL VARIABLES
URL_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Locations"
URL_FILE="Coles_URL.csv"
OUTPUT_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Output"
URL_SCRAPE_COUNT=0        
BASE_COLES_WEBSITE="https://www.coles.com.au/"
IMPLICIT_WAIT=[1,1,1]
CHROME_DRIVER_PATH="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Code\\chromedriver.exe"


class Coles_Spider_URL:

	"""
	This scraper will return all the Coles Data for the websites enlisted. 
	The Coles Spider will return a dataset which will be like this

	WE will be refreshing the links on a weekly basis to derive the information on the new links that have been
	provided to us.

	-URL Scraped From
	-Department Name
	-Department URL
	-Department Count
	-Category Name
	-Category URL
	-Category Count


	"""	
	def __init__(self,df):
		self.df=df
		self.Base_Spider()                          

	def Get_File_Name(self,out_file_name):

		file_present=[f for f in URL_FOLDER+"\\"+out_file_name if f.endswith(".csv")]
		if len(file_present)>0:
			return f"{out_file_name}-({len(file_present)-1})"
		else:
			return out_file_name

	# Build different utility scraping functions
	def Is_Coles_Running(self):
		r=requests.get(BASE_COLES_WEBSITE)
		if r.status_code==200:
			return 1
		else:
			return 0
	# This method Gets All the Department URLS

	def Get_Department_URL(self,webpage_data):
		temp_list=[]
		if len (webpage_data)==0:
			return None  		         
		temp_data=webpage_data.find_all('a',href=True)
		for info in temp_data:
			s=info['href']
			if s.find("/everything/browse/")>0 and s.find("?pageNumber")>0:
				temp_list.append(s)
		return temp_list

	# This method Gets All the Category URLS														 
	def Get_Category_URL(self,webpage_data):
		temp_cat_url=[]
		temp_cat_name=[]
		temp_cat_count=[]
		dept_name=""
		temp_dept_name=[]
		sleep(random.choice(IMPLICIT_WAIT))
		if len(webpage_data)==0:
			return None
		temp_data=webpage_data.find_all('h2',{"class":"cat-nav-heading"})
		for step_1 in temp_data:
			step_2=step_1.find_all("span",{"aria-hidden":"true"})
			for step_3 in step_2:
				dept_name=step_3.text
				if len(dept_name)>0:
					break

		temp_data=webpage_data.find_all('div',{"id":"cat-nav-list-2"})
		for t in temp_data:
			step_2=t.find_all("li",{"class":"cat-nav-item"})
			for step_3 in step_2:
				step_4=step_3.find_all("a",{"class":"clear"})
				for step_5 in step_4:
					title_span=step_5.find_all("span",{"class":"item-title"})
					count_span=step_5.find_all("span",{"class":"items-found"})
					for title in title_span:
						temp_cat_name.append(title.text)
					for count in count_span:
						temp_cat_count.append(count.text)
					temp_cat_url.append(step_5['href'])
					temp_dept_name.append(dept_name) 		#Update
		
		return temp_dept_name,temp_cat_name,temp_cat_count,temp_cat_url

	# This method gets all the Sub_Cat_URLS
	def Get_Sub_Cat_URL(self,category_url_data):
		if len(category_url_data)==0:
			raise Exception("Category URL Not Provided")
		
		temp_sub_cat_url=[]
		temp_sub_cat_name=[]
		temp_sub_cat_count=[]
		subcatname=""

		sleep(random.choice(IMPLICIT_WAIT))
		if len(category_url_data)==0:
			return None
		temp_data=category_url_data.find_all('h2',{"class":"cat-nav-heading"})
		for step_1 in temp_data:
			step_2=step_1.find_all("span",{"aria-hidden":"true"})
			for step_3 in step_2:
				subcatname=step_3.text
				if len(subcatname)>0:
					break

		temp_data=category_url_data.find_all('div',{"id":"cat-nav-list-3"})
		for t in temp_data:
			step_2=t.find_all("li",{"class":"cat-nav-item"})
			for step_3 in step_2:
				step_4=step_3.find_all("a",{"class":"clear"})
				for step_5 in step_4:
					title_span=step_5.find_all("span",{"class":"item-title"})
					count_span=step_5.find_all("span",{"class":"items-found"})
					for title in title_span:
						temp_sub_cat_name.append(title.text)
					for count in count_span:
						temp_sub_cat_count.append(count.text)
					temp_sub_cat_url.append(utils.URL_Adjustment_Categories(step_5['href']))
		
		return temp_sub_cat_name,temp_sub_cat_count,temp_sub_cat_url

	def Get_Product_Info(self,webpage_data,url_sub_cat):

		Comp_online_prod_number=[]
		Comp_Online_Prod_Name=[]
		Comp_Online_Brand_Name=[]
		Comp_Prices=[]
		Comp_Program=[]
		Comp_Savings_Sticker=[]
		Comp_Package_Size=[]
		Promo_Type=[]
		Promotion_Description=[]
		CUP_PRICE=[]

		max_page_count=PSF.Get_Max_Pages(data=webpage_data)
		for count in range(1,max_page_count+1):
			if count==1:				# Because we are already on the first website
				pass
			else:
				temp_urlx=url_sub_cat[:-len(str(count))]+str(count)				
				self.browser.get(temp_urlx)  
				sleep(random.choice(IMPLICIT_WAIT)) 
			
		#	self.browser.get("https://shop.coles.com.au/a/kellyville/everything/browse/pantry/snacks?pageNumber=1")
			Comp_online_prod_number.append(PSF.Get_Product_Number(data=self.browser.page_source,counter=count))			
			Comp_Online_Prod_Name.append(PSF.Get_Product_Name(data=self.browser.page_source,counter=count))
			Comp_Online_Brand_Name.append(PSF.Get_Brand_Info(data=self.browser.page_source,counter=count))
			Comp_Program.append(PSF.Get_Comp_Pricing_Program(data=self.browser.page_source,counter=count))
			Comp_Prices.append(PSF.Get_Comp_Price(data=self.browser.page_source,counter=count))
			Comp_Savings_Sticker.append(PSF.Get_Savings_Sticker(data=self.browser.page_source,counter=count))
			Comp_Package_Size.append(PSF.Get_Package_Size(data=self.browser.page_source,counter=count))
			CUP_PRICE.append(PSF.Get_Comp_CUP_Price(data=self.browser.page_source,counter=count))
			Promo_Type.append(PSF.Get_Comp_Promo_Type(data=self.browser.page_source,counter=count))		
			Promotion_Description.append(PSF.Get_Comp_MultiBuy_Details(data=self.browser.page_source,counter=count))

		return Comp_online_prod_number,Comp_Online_Prod_Name,Comp_Online_Brand_Name,Comp_Program,Comp_Prices,Comp_Savings_Sticker,Comp_Package_Size,CUP_PRICE,Promo_Type,Promotion_Description

	def Base_Spider(self):
		
		CATEGORY_URL_LIST=[]

		if (self.Is_Coles_Running()==1):
			pass
		else:
			raise Exception ("Coles Website Down")
			sys.exit(1)         
		
		print(f"Extracting Data for - {self.df['Site']}")
		ua=UserAgent()
		random_user_agent=ua['google chrome']
		options = webdriver.ChromeOptions()
		options.add_argument('--disable-blink-features=AutomationControlled')

		options.add_argument('log-level=3')
		self.browser = webdriver.Chrome( executable_path=CHROME_DRIVER_PATH,options=options)
		self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.browser.get(utils.Adjust_URL(self.df['URL']))                                          # Going by Store 
		sleep(random.choice(IMPLICIT_WAIT))                                  						# Including implict waits to tricke the bot
		DEPARTMENT_URL=self.Get_Department_URL(soup(self.browser.page_source,features="lxml"))
		for index,url in enumerate(DEPARTMENT_URL):
			if index>1:
				break
			else:
				self.browser.get(utils.URL_Adjustment_Categories(url))
				sleep(random.choice(IMPLICIT_WAIT)) 
				all_data=self.Get_Category_URL(soup(self.browser.page_source,features="lxml"))
				CATEGORY_URL_LIST=all_data[3]
				for sub_cat_url in CATEGORY_URL_LIST:
					self.browser.get(utils.URL_Adjustment_Categories(sub_cat_url))
					sleep(random.choice(IMPLICIT_WAIT))      
					sub_cat_data=self.Get_Sub_Cat_URL(soup(self.browser.page_source,features="lxml"))
					for families_url in sub_cat_data[2]:
						self.browser.get(families_url)
						sleep(random.choice(IMPLICIT_WAIT))
						start_time=time.time()
						product_info=self.Get_Product_Info(soup(self.browser.page_source,features="lxml"),families_url)
						print(f"Product Scraping for {families_url} took {time.time()-start_time} seconds")
						print(families_url)
						break
						print(len(product_info),type(product_info))
						sleep(5)
					break
				break
						

		self.browser.quit()

cc=pd.DataFrame(config.LOCATIONS)
Coles_Spider_URL(cc.iloc[0])









