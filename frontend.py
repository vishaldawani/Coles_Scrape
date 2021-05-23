import tkinter as tk
import pandas as pd

COLES_LOCATIONS_FILE_PATH="C:\\Users\\61433\\Desktop\\Personal Projects\\Coles\\Coles_Scrape\\Locations\\COLES_URL.csv"



df=pd.read_csv(COLES_LOCATIONS_FILE_PATH)
root=tk.Tk()
root.geometry("600x800")
complete_list=tk.Listbox(root,width=100,height=100,selectmode=tk.SINGLE)
add_btn=tk.Button(root,text="Add?")

scrollbar=tk.Scrollbar(root)
scrollbar.pack(side=tk.LEFT,fill=tk.BOTH)
for values in df['Site']:
	complete_list.insert(tk.END,values)
complete_list.config(yscrollcommand=scrollbar.set)


def add_item():
	temp_list=[]
	for i in complete_list.curselection():
		temp_list.append(i)


btn=tk.Button(root,text="Print Selected",command=add_item)
btn.pack(side="bottom")
complete_list.pack(side=tk.LEFT,fill=tk.BOTH)

root.mainloop()

