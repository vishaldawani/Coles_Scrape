"""
Developer: Vishal Dawani
Purpose: The below functions are utilised for gathering Product related functional details for Coles Related Products
The below functions related lists/or dictionaries.

"""
from bs4 import BeautifulSoup as soup
import numpy as np
from time import sleep

MAX_SLEEP_TIME=1

# Page Counters
def Get_Max_Pages(data):
	"""
	Returns:An integer value
	Purpose: To find the maximum number of pages the loop has to iterate over.

	"""
	total_count=''
	sleep(MAX_SLEEP_TIME)			
	c=data.find_all("div",{"class":"pagination-container"})
	for item in c:
		x=item.find_all("span",{"class":"number"})
		for z in x:
			total_count=z.text

	if total_count=='':
		return 1
	else:

		return np.int64(total_count)

# Product Details 
def Get_Product_Number(data,counter):
	"""
	Returns:A List
	Purpose: To find the Online Product number found on the page

	"""
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

def Get_Package_Size(data,counter):
	temp_package_size=[]
	soup_data=soup(data,features="lxml")
	for step_1 in soup_data.find_all('div',{"class":"products"}):
		if counter==1:
			step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
		else:
			step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})                       
		for step_3 in step_2:
			step_4=step_3.find_all("div",{"class":"product-main-info"})
			for step_5 in step_4:
				step_6=step_5.find_all("span",{"class":"package-size"})
				for step_7 in step_6:
					temp_package_size.append(step_7.text)
	if isinstance(temp_package_size,list) and len(temp_package_size)!=0:
		return temp_package_size
	else:
		return False

# Pricing 
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

def Get_Savings_Sticker(data,counter):
	temp_hi_lo_price=[]
	temp_savings_msg=[]
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
					step_8=step_7.find_all("span",class_="saving-container")
					if len(step_8)==0:
						temp_hi_lo_price.append("NULL")
					else:
						for step_9 in step_8:
							span_0=step_9.find_all("span",{"class":"product-save-value"})
							step_0_1=step_9.find_all("span",{"class":"product-save-prefix"})
							for span_1 in span_0:
								span_2=span_1.stripped_strings
								for span_3 in span_2:
									if len(step_0_1)!=0:
										temp_hi_lo_price.append(step_0_1[0].text.strip()+"-"+span_3)
									else:
										temp_hi_lo_price.append(span_3)


	return temp_hi_lo_price

def Get_Comp_Pricing_Program(data,counter):
	temp_program=[]
	soup_data=soup(data,features="lxml")			
	#For Promotional Color of Program 
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
			temp_program.append("NULL")
	
	if len(temp_program)!=0:
		return temp_program
	else:
		return None

def Get_Comp_Promo_Type(data,counter):
	temp_promo_type=[]
	
	def ExtractPromoType(word):
		import re
		temp_word=str(re.findall("'[('+a-zA-Z'+)]+'\\)",word))
		temp_word=temp_word.lower()
		return temp_word[temp_word.find("'")+1:temp_word.find("')")]

	soup_data=soup(data,features="lxml")
	for step_1 in soup_data.find_all("button",{"class":"button button-main"}):
		temp_text=step_1['data-colrs-if']
		temp_promo_type.append(ExtractPromoType(temp_text))

	return temp_promo_type

def Get_Comp_MultiBuy_Details(data,counter):
	soup_data=soup(data,features="lxml")
	multi_buy_Details_list=[]
	for step_1 in soup_data.find_all("button",{"class":"button button-main"}):
		qty=step_1.find_all("span",{"class":"product-qty"})
		for_text=step_1.find_all("span",{"class":"product-text"})
		price=step_1.find_all("strong",{"class":"product-price"})
		for item in qty:
			a=item.text
			if len(a)!=0:
				break
		for item in for_text:
			b=item.text
			if len(b)!=0:
				break        
		for item in price:
			c=item.text
			if len(c)!=0:
				break

		multi_buy_Details_list.append(a+" "+ b+" "+c)

	return multi_buy_Details_list

def Get_Comp_CUP_Price(data,counter):
	temp_cup_price_list=[]
	soup_data=soup(data,features="lxml")
	for step_1 in soup_data.find_all('div',{"class":"products"}):
		if counter==1:
			step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate"})
		else:
			step_2=step_1.find_all("div",{"class":"colrs-animate tile-animate tile-stagger"})                       
		for step_3 in step_2:
			step_4=step_3.find_all("div",{"class":"product-info"})
			for step_5 in step_4:
				step_6=step_5.find_all("span",{"class":"package-price"})
				for step_7 in step_6:
					temp_cup_price_list.append(step_7.text)
	return temp_cup_price_list
