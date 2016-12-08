import gspread

def login():
    gc = gspread.login('user','passwd')  
    return gc




