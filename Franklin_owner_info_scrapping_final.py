# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:45:44 2019

@author: adityak
"""

import numpy as np
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support.ui import Select
import os

df = r"D:\From_D_drive\PROJECTS\Sales_Data\Sales_Dec_2019\Franklin\FranklinCountyFL-20200120.xlsx"
data = pd.read_excel(df)
data.columns.str.strip()
data.columns.str.replace(' ','_')

headers = []
for col in data.columns: 
    headers.append(col)
    print(col)

data['Sale_Date'] = pd.to_datetime(data.Sale_Date)
#df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')
mask = (data['Sale_Date'] > '2019-12-01') & (data['Sale_Date'] <= '2019-12-31')
new_df = (data.loc[mask])

mask1 = (new_df['Sale_Price'] >= 100) & (data['Sale_Price'] <= 99999999)
new_df1 = (new_df.loc[mask1])

mask2 = (new_df1['Qualified_Sales'] =="Qualified")
new_df2 = (new_df1.loc[mask2])

parcel_no = []
########parcel_no[0][0]######
parcel_no.append(new_df2['Parcel_ID'].tolist())

new_df2 = new_df2[["Parcel_ID","Address","Sale_Date","Sale_Price"]]
new_df2.to_excel(r"D:\From_D_drive\PROJECTS\Sales_Data\Sales_Dec_2019\Franklin\Franklin_filtered.xlsx")
new_df2.to_csv(r"D:\From_D_drive\PROJECTS\Sales_Data\Sales_Dec_2019\Franklin\Franklin_filtered.txt")
cnty = "FRANKLIN"

options = webdriver.ChromeOptions()
options.headless=True
final_array = [["Parcel_no","CountyName","Owner_Name1",'Owner_Name2',"Address1","Address2","City_State_Zip","Sale_date","Sale_Price"]]
for pp in parcel_no[0]:
    driver = webdriver.Chrome(r"C:\Users\adityak.EXZEO\Downloads\Extra\chromedriver_win32\chromedriver.exe",chrome_options=options)
    driver.get('https://qpublic.schneidercorp.com/Application.aspx?AppID=816&LayerID=14540&PageTypeID=4&PageID=6407&Q=1656862162&KeyValue='+pp)
    driver.maximize_window()
    Chk_1 = driver.find_element_by_xpath('//*[@id="appBody"]/div[4]/div/div/div[2]/div[2]/a[1]')
    Chk_1.click()
    try:
        try:
            p_owner = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl01_ctl01_lstPrimaryOwner_ctl00_lblPrimaryOwnerName_lblSearch"]')
            m = p_owner.text
            p_address = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl01_ctl01_lstPrimaryOwner_ctl00_lblPrimaryOwnerAddress"]')
            n=p_address.text.split('\n')
#            o = m+' '+n
#            b=o.replace('\n',' ')
            sale_Date=driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl06_ctl01_grdSales"]/tbody/tr[1]/td[2]')
            date = sale_Date.text
            sale_price = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl06_ctl01_grdSales"]/tbody/tr[1]/td[3]')
            price = sale_price.text
            pr = price.replace(',','')
            prr=pr.replace('$','')
            print (pp+"---",m)
            if len(n)==2:
                final_array.append([pp,cnty,m,"",n[0],n[1].split(',')[0],n[1].split(',')[-1],date,prr])
            else:
                final_array.append([pp,cnty,m,n[0],n[1],n[2].split(',')[0],n[2].split(',')[-1],date,prr])
            driver.close()
        except:
            p_owner = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl01_ctl01_lstPrimaryOwner_ctl00_lblPrimaryOwnerName_lnkSearch"]')
            m = p_owner.text
            p_address = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl01_ctl01_lstPrimaryOwner_ctl00_lblPrimaryOwnerAddress"]')
            n=p_address.text.split('\n')
#            o = m+' '+n
#            b=o.replace('\n',' ')        
            sale_Date=driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl06_ctl01_grdSales"]/tbody/tr[1]/td[2]')
            date = sale_Date.text
            sale_price = driver.find_element_by_xpath('//*[@id="ctlBodyPane_ctl06_ctl01_grdSales"]/tbody/tr[1]/td[3]')
            price = sale_price.text
            pr = price.replace(',','')
            prr=pr.replace('$','')
            print (pp+"---",m)
            
            if len(n)==2:
                final_array.append([pp,cnty,m,"",n[0],n[1].split(',')[0],n[1].split(',')[-1],date,prr])
            else:
                final_array.append([pp,cnty,m,n[0],n[1],n[2].split(',')[0],n[2].split(',')[-1],date,prr])
            driver.close()
    except:
        pass
        driver.close()
        

with open(r"D:\From_D_drive\PROJECTS\Sales_Data\Sales_Dec_2019\Franklin\Franklin_owner_info_final.csv", 'w',newline='') as f:
   writer = csv.writer(f)
   writer.writerows(final_array)
   
with open(r"D:\From_D_drive\PROJECTS\Sales_Data\Sales_Dec_2019\Franklin\Franklin_owner_info_final.txt", 'w',newline='') as f:
   writer = csv.writer(f)
   writer.writerows(final_array)