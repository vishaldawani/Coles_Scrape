"""
This part of Python code will combine several workers to improve the speed for the scrapes for Categories.

"""

#Will run as a base_point for the threading 
from step_1_category import Coles_Spider_URL  
from step_1_category import URL_FOLDER
from step_1_category import URL_FILE
import config


import pandas as pd
import threading
import math
import os
import numpy as np
from time import sleep

df=pd.DataFrame(config.LOCATIONS)
print(df)


INPUT_FILE_NAME = URL_FILE
NUM_WORKERS = 15

line_count = int(len(pd.read_csv(URL_FOLDER+"//"+INPUT_FILE_NAME)) / NUM_WORKERS)	
def worker(num,line_count):
    Coles_Spider_URL(URL_FOLDER,URL_FILE,num,int(num),int(line_count))
    return

threads = []
remaining_urls = 0

for i in range(NUM_WORKERS):
	if i==NUM_WORKERS-1:
			remaining_urls=int(len(pd.read_csv(URL_FOLDER+"//"+INPUT_FILE_NAME))-(NUM_WORKERS*line_count))
	start_counter=i*line_count
	end_counter=((i+1)*line_count)-1+remaining_urls
#	t = threading.Thread(target=worker, args=(start_counter,end_counter))
#	threads.append(t)
#	t.start()




