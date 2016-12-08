from selenium.common.exceptions import NoSuchElementException
import time

def update(updateWorksheet, backers, moneyRaised, daysLeft, campaignState):
    #cast daysLet now is a string
	daysLeft = int(daysLeft.split()[0])
	lastCell = updateWorksheet.acell('A1').value 
	print("campaign state: ", campaignState)
	print("daysLeft: ", daysLeft)
	
	if campaignState == 0:
		updateWorksheet.update_acell('C'+ str(lastCell), daysLeft)
		updateWorksheet.update_acell('D'+ str(lastCell), backers)
		updateWorksheet.update_acell('E'+ str(lastCell), moneyRaised)
		updateWorksheet.update_acell('B'+ str(lastCell), time.strftime("%c"))
		print("updated cell:", int(lastCell) + 1)
		updateWorksheet.update_acell('A1', str(int(lastCell) + 1) )
	
	if campaignState == -4: 
		updateWorksheet.update_acell('I7', 'CAMPAIGN FUNDED')
		print("Campaign FUNDED")
		updateWorksheet.update_acell('A1', 'DONE')
	
	if campaignState == -2:
		updateWorksheet.update_acell('I7', 'CAMPAIGN CANCELLED')
		print("Campaign CANCELLED")
		updateWorksheet.update_acell('A1', 'DONE')
	
	if campaignState == -3:
		updateWorksheet.update_acell('I7', 'CAMPAIGN UNSUCCESSFUL')
		print("Campaign UNSUCCESSFUL")
		updateWorksheet.update_acell('A1', 'DONE')	
   
#función de actualización para cambiar la manera de revisar los datos
#########################################

def create(titleProject, sh, backersC, moneyRaisedC, moneyPledged, daysLeftC, url):
    #create a new worksheet (can not be bigger than 100 characters)
	if len(titleProject) > 100:
		worksheet = sh.add_worksheet(title=titleProject[:100], rows="100", cols="20")
	else:
		worksheet = sh.add_worksheet(title=titleProject, rows="100", cols="20")
        
	worksheet.update_acell('C2', 'DAYS LEFT')
	worksheet.update_acell('D2', 'BACKERS')
	worksheet.update_acell('E2', 'MONEY RAISED')
	worksheet.update_acell('G2', 'MONEY PLEDGED')
	worksheet.update_acell('G3', moneyPledged)
	worksheet.update_acell('H2', 'URL')
	worksheet.update_acell('H3', url)
	worksheet.update_acell('C3', daysLeftC)
	worksheet.update_acell('D3', backersC)
	worksheet.update_acell('E3', moneyRaisedC)
	worksheet.update_acell('B3', time.strftime("%c"))
	worksheet.update_acell('A1', 'G3') #esta celda sirve para poder hacer el update,
									#se fija en la celda A1 para saber donde tiene 
									#que meter la información
	print('new project added')
	
#########################################
def dataCollector(webdriver,driver,urlProject):
    #here is the driver where we are going to 
	driver.get(urlProject)
	titleProject = driver.title

	backers = str(driver.find_element_by_css_selector('div#backers_count.num.h1.bold').text)
	moneyRaised = str(driver.find_element_by_css_selector('div#pledged.num.h1.bold.nowrap').text)

	found = False
	while not found:
		try:
			moneyPledged = str(driver.find_element_by_css_selector('span.money.usd.no-code').text)
			found = True
		except NoSuchElementException:
			moneyPledged = str(driver.find_element_by_css_selector('span.mobile-hide').text)
			found = True
		except NoSuchElementException:
			moneyPledged = str(driver.find_element_by_css_selector('span.money.aud.no-code').text)
			found = True

		foundDays = False
	while not foundDays:
		try:
			campaignState = -1
			daysLeft = '0'
			fundingText = str(driver.find_element_by_css_selector('h3.normal.mb1').text)
				
			if fundingText == 'Funding Unsuccessful':
				campaignState = -3
			
			elif fundingText == 'Funding Cancelled':
				campaignState = -2
			
			elif fundingText == 'Funded!':
				campaignState = -4
			foundDays = True
			
		except NoSuchElementException:
			campaignState = 0
			daysLeft = str(driver.find_element_by_css_selector('div.ksr_page_timer.poll.stat').text)
			foundDays = True
			
		except NoSuchElementException:
			campaignState = 0
			daysLeft = str(driver.find_element_by_css_selector('div.poll.stat').text)
			foundDays = True
	
	dataList = [backers, moneyRaised, moneyPledged, daysLeft, titleProject, campaignState]

	print("campaign added with url", urlProject)
	return dataList
 
