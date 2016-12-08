from selenium import webdriver
import gspread
import time
from passwd import login    

#login Drive
gc = login() 
#open the spreadsheet
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1w9yC4O1-lb87pCv8kudxyJiUak4akqJvhr7LeqYKv4o/edit#gid=2030862229")

worksheetList = sh.worksheets()	
		
j=0
while j != len(worksheetList):
	updateWorksheet = sh.get_worksheet(j)
	for i in range(4,63):
		if (updateWorksheet.acell('C'+ str(i)).value == ""):
			updateWorksheet.update_acell('A1', i)
			print("updated cell A1: ", i)
			break
	j+=1
