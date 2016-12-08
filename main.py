from selenium import webdriver
from worksheetFunctions import dataCollector
from worksheetFunctions import update
from worksheetFunctions import create    
from index import indexMaker
from passwd import login
import gspread
import time
import os

#login Drive
gc = login() 
#open de spreadsheet
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1w9yC4O1-lb87pCv8kudxyJiUak4akqJvhr7LeqYKv4o/edit#gid=375195005")
##############################################################
indexList = indexMaker(sh)
##############################################################
driver = webdriver.Firefox()

k = 0
while k != len(indexList):
    dataList = dataCollector(webdriver,driver,indexList[k])
    if len(dataList[4]) > 100:
        dataList[4] = dataList[4][:100]
    if dataList[4] not in str(sh.worksheets()):
      create(dataList[4], sh, dataList[0], dataList[1],dataList[2], dataList[3],indexList[k])
    k+=1
    
driver.close()  
##############################################################   
#update
##############################################################




