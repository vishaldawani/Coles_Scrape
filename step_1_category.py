
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
from bs4 import BeautifulSoup as soup
from time import sleep
import os
import pandas as pd
import requests
import sys
import utils
import random
import numpy as np

# DECLARE GLOBAL VARIABLES
OUTPUT_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Output\\Category_Output"
URL_SCRAPE_COUNT=0        
BASE_COLES_WEBSITE="https://www.coles.com.au/"
IMPLICIT_WAIT=[1,2,5]
CHROME_DRIVER_PATH="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Code\\chromedriver.exe"


class Coles_Spider_URL:
	def __init__(self,df,output_name,range_start,range_end):
		temp_df=df
		self.df=temp_df.iloc[range_start:range_end+1]
		self.df.index=np.arange(len(self.df))
		self.worker_index=output_name
		print(self.df)
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
														 
	def Get_Category_URL(self,webpage_data,post_code,url_scraped_from):
		temp_cat_url=[]
		temp_cat_name=[]
		temp_cat_count=[]
		dept_name=""
		temp_dept_name=[]
		temp_post_code=[]
		temp_url_scraped_from=[]
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
					temp_post_code.append(post_code)
					temp_url_scraped_from.append(url_scraped_from)
		
		return temp_url_scraped_from,temp_post_code,temp_dept_name,temp_cat_name,temp_cat_count,temp_cat_url

	def PopulateLists(self,data_list):
		temp_list=[]
		if isinstance(data_list, list):
			for num in range(len(data_list)):
				for item in data_list[num]:
					temp_list.append(item)

			return temp_list
		else:
			raise Exception ("Invalid List Type Object")

	def Base_Spider(self):
		temp_df=self.df
		URL_SCRAPED_FROM=[]
		POST_CODE=[]		
		DEPARTMENT_NAME=[]
		CAT_NAME=[]
		CAT_COUNT=[]
		CATEGORY_URL_LIST=[]
		DEPARTMENT_NAME_LIST=[]
		URL_SCRAPED_FROM_LIST=[]
		
		if (self.Is_Coles_Running()==1):
			pass
		else:
			raise Exception ("Coles Website Down")
			sys.exit(1)         
		
		options = webdriver.ChromeOptions()
		options.add_argument('--disable-blink-features=AutomationControlled')
		options.add_argument('--headless')
		options.add_argument('log-level=3')
		self.browser = webdriver.Chrome( executable_path=CHROME_DRIVER_PATH,options=options)
		self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


		for index,url in enumerate(temp_df['URL']):
			print(f"Extracting Data for - {temp_df['Site'][index]}")
			self.browser.get(utils.Adjust_URL(url))                                          # Going by Store 
			sleep(random.choice(IMPLICIT_WAIT))                                     # Including implict waits to tricke the bot
			DEPARTMENT_URL=self.Get_Department_URL(soup(self.browser.page_source,features="lxml"))
			for url in DEPARTMENT_URL:
				self.browser.get(utils.URL_Adjustment_Categories(url))
				sleep(3)
				all_data=self.Get_Category_URL(soup(self.browser.page_source,features="lxml"),temp_df['Postcode'][index],temp_df['Site'][index])
				URL_SCRAPED_FROM.append(all_data[0])
				POST_CODE.append(all_data[1])
				DEPARTMENT_NAME.append(all_data[2])
				CAT_NAME.append(all_data[3])
				CAT_COUNT.append(all_data[4])
				CATEGORY_URL_LIST.append(all_data[5])
				

			temp_listx_1=self.PopulateLists(URL_SCRAPED_FROM)		# URL_SCRAPED_FROM
			temp_listx_2=self.PopulateLists(POST_CODE)				#POST_CODE
			temp_listx_3=self.PopulateLists(DEPARTMENT_NAME)		#DEPARTMENT_NAME
			temp_listx_4=self.PopulateLists(CAT_NAME)				#CATEGORY_NAME
			temp_listx_5=self.PopulateLists(CAT_COUNT)				#CATEGORY_COUNT
			temp_listx_6=self.PopulateLists(CATEGORY_URL_LIST)		#CATEGORY_URL_LIST
			
			Data_Dict={
					"URL_SCRAPED_FROM":temp_listx_1,
					"POST_CODE":temp_listx_2,
					"DEPARTMENT":temp_listx_3,
					"CATEGORY_NAME":temp_listx_4,
					"CATEGORY_COUNT":temp_listx_5,
					"CATEGORY_URL":temp_listx_6
					}
			df=pd.DataFrame(Data_Dict)
			df.to_csv(OUTPUT_FOLDER+"\\"+temp_df['Site'][index]+".csv")
			print(f"{temp_df['Site'][index]} - Data Exported Successfully - Remaining {len(temp_df['Site'])-index}")

			URL_SCRAPED_FROM.clear()
			POST_CODE.clear()
			DEPARTMENT_NAME.clear()
			CAT_NAME.clear()
			CAT_COUNT.clear()
			CATEGORY_URL_LIST.clear()
			Data_Dict.clear()

		self.browser.quit()











