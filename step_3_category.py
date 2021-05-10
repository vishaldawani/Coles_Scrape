""" This step of the model will now scrape product level
information for all the files that have 
been exported. The aim of this step is to finally derive the product level details
"""


# Imports
import os
import pandas as pd
import config
import utils
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from step_1_category import CHROME_DRIVER_PATH,IMPLICIT_WAIT
import random
from time import sleep

# VARIABLES
DATA_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Output\\Category_Output"
OUTPUT_FOLDER="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Output\\Category_Output"
COMBINED_FILE_NAME="Departmental.csv"
USE_EXISTING_FILE=True												 	# SETTING THIS TO FALSE WILL GENERATE A NEW FILE OR ELSE WILL READ THE PREVIOUS DEPARTMENTAL CSV


"""
 REQUIRED DATA_STRUCTURE
 ---Iterate through Each Sub Category whilst capturing the Additional Details 

 	Product  - Pricing - Area - Dimensions  (Sub Cat, Cat, Department)
 	


	

"""


class Coles_Product_Spider():
	def __init__(self):
		self.temp_dict=dict(self.Store_Departmental_Files())					# THIS CLEANS UP + PRODUCES A DEPARTMENTAL FILE
		self.Spider()

	def Store_Departmental_Files(self):
		if USE_EXISTING_FILE==False:
			utils.Removes_Departmental_Files(INPUT_FOLDER=DATA_FOLDER, OUTPUT_FOLDER=OUTPUT_FOLDER, OUTPUT_FILE_NAME=COMBINED_FILE_NAME)
		self.df=utils.Combine_Departmental_CSV(INPUT_FOLDER=DATA_FOLDER, OUTPUT_FOLDER=OUTPUT_FOLDER, OUTPUT_FILE_NAME=COMBINED_FILE_NAME)
		return self.df

	### Below functions are used for yielding the data from Coles Page data
	@staticmethod
	def Get_Sub_Cat_Links(self,page_data):
		pass

	def Product_Info(self,page_data):
		pass

	def Pricing_Info(self,page_data):
		pass

	def Program_Selection(self,page_data):
		pass

	def Product_Dimensions(self,page_data):
		pass

	def Get_Max_Page_Count(self,page_data):
		pass

	def Subcat_Name(self,page_data):
		pass

	def Cat_Name(self,page_data):
		pass

	


	def Spider(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--disable-blink-features=AutomationControlled')
		options.add_argument('log-level=3')
		self.browser = webdriver.Chrome( executable_path=CHROME_DRIVER_PATH,options=options)
		self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



		data_dict=self.temp_dict
		for item in enumerate(data_dict.keys()): 
			self.browser.get(data_dict['Adjusted_URL'][item])
			sleep(random.choice[IMPLICIT_WAIT])
			webpage_data=soup(self.browser.page_source,features="lxml")




















Coles_Product_Spider()