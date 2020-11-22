import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os, time

def checkDir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def setWebDriver(chromedriverPath, viewChrome=False):
    chrome_options = webdriver.ChromeOptions()
    userProfile = os.path.abspath("./cache")
    chrome_options.add_argument("user-data-dir={}".format(userProfile))
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    if not viewChrome: 
        chrome_options.add_argument('--headless')
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriverPath)
    
######## Plot
def plotLine(x, y, title=None, figSize=(15, 5)):
    plt.figure(figsize=figSize)
    if title != None: plt.title(title)    
    plt.ylabel("Number")
    plt.xlabel("Year") 
    plt.plot(list(map(str,x)), y)  

def imgShow():   
    plt.show()   

def imgSave(savePath="./saveData/images/", saveFileName='img.png'):
    checkDir(savePath)
    plt.savefig(savePath + saveFileName)

######## Nums 
def getNumByYear(sortedYears, basicUrl, driver):
    nums = []
    for index, year in enumerate(sortedYears):
        if index+1 < len(sortedYears):
            finalUrl = basicUrl.format(str(year) + '&as_yhi=' + str(sortedYears[index+1] - 1))
            driver.get(finalUrl)
            element = driver.find_element_by_id('gs_ab_md')
            data = element.text
            if data.split()[0] != 'About':
                number = data.split()[0]
            else:
                number = data.split()[1]
            nums.append(int("".join(number.split(','))))
            print('year: {}, about {} results'.format(year, number)) 
            time.sleep(2)
    return nums

def saveNums(years, nums, savePath='./saveData/numsCsv/', saveFileName='num.csv'):
    checkDir(savePath)
    dataDf = pd.DataFrame()
    dataDf['Year'] = years
    dataDf['Number'] = nums
    dataDf.to_csv(savePath + saveFileName)
