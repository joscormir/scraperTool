import urllib.request
import gspread
import re

def indexMaker(sh):
    ##############################################################
    #TotalProjects
    httpTotalProjectsRaw= str(urllib.request.urlopen("https://www.kickstarter.com/discover/advanced?category_id=16&woe_id=0&sort=magic").read())
    urlList = list(set(re.findall('href="/projects[^"]*?ref', httpTotalProjectsRaw)))
    #print(urlList)

    ##############################################################
    #Popularity
    httpPopularProjectsRaw = str(urllib.request.urlopen("https://www.kickstarter.com/discover/advanced?category_id=16&sort=popularity").read())
    urlPopularList = list(set(re.findall('href="/projects[^"]*?ref', httpPopularProjectsRaw)))
    #print(urlPopularList)
         
    #############################################################·

    worksheetIndex = sh.worksheet("Index")
    sh.del_worksheet(worksheetIndex)
    worksheetIndex = sh.add_worksheet(title="Index", rows="100", cols="20")

    ##############################################################
    compList = list(set(urlList)& set(urlPopularList))

    p = 0
    q = 0
    defList = [0]*(len(urlList)-1)
    while p != len(urlList)-1:
        defList[p] = "https://www.kickstarter.com/" + urlList[p][6:-4]
        worksheetIndex.update_acell('C'+str(p+1), defList[p])
        if urlList[p] == compList[q] and q != len(compList):
            worksheetIndex.update_acell('I'+str(p+1), '*')
            q+=1
        p+=1
        print("this is the number of project",p)   

    return defList
    
               
    

