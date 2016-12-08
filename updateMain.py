from selenium import webdriver
from worksheetFunctions import dataCollector
import gspread
import time
from worksheetFunctions import update
from passwd import login    

start = time.time()
#login Drive
gc = login() 
#open the spreadsheet
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1w9yC4O1-lb87pCv8kudxyJiUak4akqJvhr7LeqYKv4o/edit#gid=33883425")
#sleep a while to not collapse 
time.sleep(1)
driver = webdriver.Firefox()

worksheetList = sh.worksheets()

j=0
while j != len(worksheetList):
	updateWorksheet = sh.get_worksheet(j)
	if (updateWorksheet.acell('H3').value != ''):
		urlWSUpdate = updateWorksheet.acell('H3').value
		dataupdateList = dataCollector(webdriver, driver, urlWSUpdate)
		update(updateWorksheet, dataupdateList[0], dataupdateList[1], dataupdateList[3], dataupdateList[5])
	j+=1
################################################################
driver.close()        
end = time.time()
print(end - start)
