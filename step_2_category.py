"""
This part of Python code will combine several workers to improve the speed for the scrapes for Categories.
This forms the second part of the code 

"""

#Will run as a base_point for the threading 
from step_1_category import Coles_Spider_URL  
import config


import pandas as pd
import threading
import math
import os
import numpy as np
from time import sleep

df=pd.DataFrame(config.LOCATIONS)
NUM_WORKERS = 2

line_count = int(len(df) / NUM_WORKERS)	
def worker(num,line_count):
    Coles_Spider_URL(df,num,int(num),int(line_count))
    return

threads = []
remaining_urls = 0

for i in range(NUM_WORKERS):
	if i==NUM_WORKERS-1:
			remaining_urls=int(len(df)-(NUM_WORKERS*line_count))
	else:
		pass
	start_counter=i*line_count
	end_counter=((i+1)*line_count)-1+remaining_urls
	print(start_counter,end_counter)
	t = threading.Thread(target=worker, args=(start_counter,end_counter))
	threads.append(t)
	t.start()




