
# Adjusts the URLS by removing home and suffixing with browse
def Adjust_URL(non_adjusted_url):
    print(non_adjusted_url)
    temp_url=non_adjusted_url[:-4]+"everything/browse"
    return temp_url

# Adjusts the URLS by removing home and suffixing with browse
def URL_Adjustment_Categories(non_adjusted_url):
    temp_url="https://shop.coles.com.au"+non_adjusted_url
    return temp_url

# Converts the Count and examines the total cat count
def Check_Count(temp_num):
    if isinstance(temp_num,int) or isinstance(temp_num,float):
        return temp_num
    if isinstance(temp_num,str):
        if temp_num.find(",")>0:
            return float(temp_num.replace(",",""))
        else:
            return float(num)

# Removes the Departmental CSV needed in Step 3
def Removes_Departmental_Files(INPUT_FOLDER,OUTPUT_FOLDER,OUTPUT_FILE_NAME):
    import os
    store_departmental_files=[f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv') and f!=OUTPUT_FILE_NAME]           # CHECKS FOR 
    combined_departmental_file=[f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv') and f==OUTPUT_FILE_NAME]

    if len(store_departmental_files)!=0:
        print(f"{len(store_departmental_files)} - Data Files Found")
    else:
        raise Exception ("Files Not Found")

    if len(combined_departmental_file)>0:
        os.remove(INPUT_FOLDER+"\\"+OUTPUT_FILE_NAME)
        print(f"{OUTPUT_FILE_NAME} Removed")
    else:
        pass

# Adds the Departmental CSV needed for Step 3.
def Combine_Departmental_CSV(INPUT_FOLDER,OUTPUT_FOLDER,OUTPUT_FILE_NAME):
    import pandas as pd
    import os
    def Adjust_Category_URL(category_url):
        if category_url=="#":
            return "NULL"
        result="https://shop.coles.com.au"+category_url
        return result

    files=[f for f in os.listdir(INPUT_FOLDER) if f.endswith('.csv')]
    temp_list=[]
    for file in files:
        temp_df=pd.read_csv(INPUT_FOLDER+"\\"+file,index_col=None,header=0,delimiter=',')
        temp_list.append(temp_df)
    required_frame=pd.concat(temp_list,axis=0,ignore_index=True)
    required_frame['Adjusted_URL']=required_frame.apply(lambda x:Adjust_Category_URL(x.CATEGORY_URL),axis=1)    
    required_frame=required_frame.drop(columns=['Unnamed: 0','CATEGORY_URL'])
    return required_frame

def PopulateLists(data_list):
    temp_list=[]
    if isinstance(data_list, list):
        for num in range(len(data_list)):
            for item in data_list[num]:
                temp_list.append(item)

        return temp_list
    else:
        raise Exception ("Invalid List Type Object")

def Adjust_Sub_Cat_URL(url,total_count):
    for count in range(1,max_page_count+1):
        print(url_data[:len(count)])    


