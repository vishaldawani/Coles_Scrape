
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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as soup
from time import sleep
import os
import pandas as pd
import requests
import sys
import utils
import random
import numpy as np
import config


# DECLARE GLOBAL VARIABLES
URL_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Locations"
URL_FILE="Coles_URL.csv"
OUTPUT_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Output"
URL_SCRAPE_COUNT=0        
BASE_COLES_WEBSITE="https://www.coles.com.au/"
IMPLICIT_WAIT=[1,2,5]
CHROME_DRIVER_PATH="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Code\\chromedriver.exe"


class Coles_Spider_URL:
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
		sleep(3)
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

		sleep(3)
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
		online_prod_number=[]
		Online_Prod_Name=[]
		Online_Brand_Name=[]
		Comp_Prices=[]
		Comp_Program=[]
		HiLoPrice=[]

		def Get_Max_Pages(data):
			total_count=''
			sleep(2)			
			c=data.find_all("div",{"class":"pagination-container"})
			for item in c:
				x=item.find_all("span",{"class":"number"})
				for z in x:
					total_count=z.text

			if total_count=='':
				return 1
			else:

				return np.int64(total_count)

		def Get_Product_Number(data,counter):
			temp_prod_num=[]
			soup_data=soup(data,features="lxml")
			for step_1 in soup_data.find_all('div',{"class":"products"}):
				if counter==1:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
				else:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})					
				for step_3 in step_2:
					step_4=step_3.find_all("div",{"class":"product-main-info"})
					for step_5 in step_4:
						step_6_prod=step_5.find("h3",class_="product-title")["data-partnumber"]
						temp_prod_num.append(step_6_prod)
			
			if isinstance(temp_prod_num,list):
				return temp_prod_num
			else:
				raise Exception("Product Numbers not Found")

		def Get_Product_Name(data,counter):
			Online_Product_Name=[]
			soup_data=soup(data,features="lxml")
			for step_1 in soup_data.find_all('div',{"class":"products"}):
				
				if counter==1:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
				else:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})		

				for step_3 in step_2:
					step_4=step_3.find_all("div",{"class":"product-main-info"})
					for step_5 in step_4:
						step_6_prod=step_5.find_all("h3",class_="product-title")
						for step_7 in step_6_prod:
							article_name=step_7.find_all("span",{"class":"product-name"})
							for name in article_name:
								if len(name)>0:
									Online_Product_Name.append(name.text)
									break

			if isinstance(Online_Product_Name,list):
				return Online_Product_Name
			else:
				raise Exception("Product Names not Found")

		def Get_Brand_Info(data,counter):
			Online_Brand_Info=[]
			soup_data=soup(data,features="lxml")
			for step_1 in soup_data.find_all('div',{"class":"products"}):
				if counter==1:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
				else:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})						

				for step_3 in step_2:
					step_4=step_3.find_all("div",{"class":"product-main-info"})
					for step_5 in step_4:
						step_6_prod=step_5.find_all("h3",class_="product-title")
						for step_7 in step_6_prod:
							brands=step_7.find_all("span",{"class":"product-brand"})
							for brand in brands:
								if len(brand)>0:
									Online_Brand_Info.append(brand.text)
									break

			if isinstance(Online_Brand_Info,list):
				return Online_Brand_Info
			else:
				raise Exception("Brands not Found")

		def Get_Comp_Price(data,counter):
			tempPrices=[]
			soup_data=soup(data,features="lxml")
			for step_1 in soup_data.find_all('div',{"class":"products"}):
				if counter==1:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
				else:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})						
				for step_3 in step_2:
					step_4=step_3.find_all("div",{"class":"product-main-info"})
					for step_5 in step_4:
						step_6_prod=step_5.find_all("span",class_="product-pricing-info")
						for step_7 in step_6_prod:
							step_8=step_7.find_all("span",class_="price-container")
							for step_9 in step_8:
								dollar_values=step_9.find_all("span",{"class":"dollar-value"})
								cent_values=step_9.find_all("span",{"class":"cent-value"})
								currency_Values=step_9.find_all("span",{"class":"currency-sign"})                    
								for i in range(len(dollar_values)):
									tempPrices.append(currency_Values[i].text+dollar_values[i].text+cent_values[i].text)
            
			if len(tempPrices)!=0:
				return tempPrices
			else:
				return  Exception ("Invalid competitor Pricing")

		def Get_Comp_Pricing_Program(data,counter):
			temp_program=[]
			soup_data=soup(data,features="lxml")			
			for step_1 in soup_data.find_all("header",{"role":"presentation","class":"product-header"}):
				if step_1.find("div",class_="product-icons"):
					step_1_1=step_1.find("div",class_="product-icons")
					x=step_1_1.contents[2]
					x1=x['class']
					for y in x1:
						if y=="icon":
							pass
						else:
							temp_program.append(y)
				else:
					temp_program.append("white")		

			if len(temp_program)!=0:
				return temp_program
			else:
				return None

		def Get_Hi_Lo_Price(data,counter):
			temp_hi_lo_price=[]
			soup_data=soup(data,features="lxml")
			sleep(2)
			for step_1 in soup_data.find_all('div',{"class":"products"}):
				if counter==1:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
				else:
					step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})                       
				for step_3 in step_2:
					step_4=step_3.find_all("div",{"class":"product-main-info"})
					for step_5 in step_4:
						step_6_prod=step_5.find_all("span",class_="product-pricing-info")
						for step_7 in step_6_prod:
							step_8=step_7.find_all("span",class_="saving-container")
							if len(step_8)==0:
								temp_hi_lo_price.append("NULL")
							else:
								for step_9 in step_8:
									span_0=step_9.find_all("span",{"class":"product-save-value"})
									for span_1 in span_0:
										span_2=span_1.stripped_strings
										for span_3 in span_2:
											temp_hi_lo_price.append(span_3)

			return temp_hi_lo_price

		max_page_count=Get_Max_Pages(data=webpage_data)
		
		for count in range(1,max_page_count+1):
			if count==1:				# Because we are already on the first website
				pass
			else:
				temp_urlx=url_sub_cat[:-len(str(count))]+str(count)				
				self.browser.get(temp_urlx)  
				sleep(2) 

			online_prod_number.append(Get_Product_Number(data=self.browser.page_source,counter=count))
			Online_Prod_Name.append(Get_Product_Name(data=self.browser.page_source,counter=count))
			Online_Brand_Name.append(Get_Brand_Info(data=self.browser.page_source,counter=count))
			Comp_Prices.append(Get_Comp_Price(data=self.browser.page_source,counter=count))
			Comp_Program.append(Get_Comp_Pricing_Program(data=self.browser.page_source,counter=count))
			HiLoPrice.append(Get_Hi_Lo_Price(data=self.browser.page_source,counter=count))

		return online_prod_number,Online_Prod_Name,Online_Brand_Name,Comp_Prices,Comp_Program

	def Base_Spider(self):
		
		CATEGORY_URL_LIST=[]

		if (self.Is_Coles_Running()==1):
			pass
		else:
			raise Exception ("Coles Website Down")
			sys.exit(1)         
		
		print(f"Extracting Data for - {self.df['Site']}")
		ua=UserAgent()
#		random_user_agent=ua.random
		random_user_agent=ua['google chrome']

		print(random_user_agent)

		options = webdriver.ChromeOptions()
		options.add_argument('--disable-blink-features=AutomationControlled')
#		options.add_argument(f'user-agent={random_user_agent}')
#		options.add_argument('--headless')
		options.add_argument('log-level=3')

		
		self.browser = webdriver.Chrome( executable_path=CHROME_DRIVER_PATH,options=options)
		self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.browser.get(utils.Adjust_URL(self.df['URL']))                                          # Going by Store 
		sleep(random.choice(IMPLICIT_WAIT))                                  						# Including implict waits to tricke the bot
		DEPARTMENT_URL=self.Get_Department_URL(soup(self.browser.page_source,features="lxml"))
		for index,url in enumerate(DEPARTMENT_URL):
			if index>5:
				break
			else:
#				self.browser.get('https://shop.coles.com.au/a/wentworth-point/everything/browse/convenience-meals-4390554?pageNumber=1')
				self.browser.get(utils.URL_Adjustment_Categories(url))
				sleep(random.choice(IMPLICIT_WAIT)) 
				all_data=self.Get_Category_URL(soup(self.browser.page_source,features="lxml"))
				CATEGORY_URL_LIST=all_data[3]
				for sub_cat_url in CATEGORY_URL_LIST:
					self.browser.get(utils.URL_Adjustment_Categories(sub_cat_url))
					sleep(2)
					sub_cat_data=self.Get_Sub_Cat_URL(soup(self.browser.page_source,features="lxml"))
					for families_url in sub_cat_data[2]:
						self.browser.get(families_url)
						sleep(random.choice(IMPLICIT_WAIT)) 
						product_info=self.Get_Product_Info(soup(self.browser.page_source,features="lxml"),families_url)
						print(type(product_info))
	
		self.browser.quit()

cc=pd.DataFrame(config.LOCATIONS)
Coles_Spider_URL(cc.iloc[1])










