from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import logging
import threading 
from concurrent.futures import ThreadPoolExecutor
lck = threading.Lock()
# Configure selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome("C:/chromedriver",options=chrome_options)


def filterPageNumber(string):
    stringRet=""
    try:
        for i in range(string.find("of")+3,len(string)):
            stringRet+=string[i]
    except Exception as err:
        logging.error(err)
    if stringRet=="":
        logging.error("Page Number is Empty")
    return stringRet

def validationCheck(dataDictionary):
    productDetails={}
    try:
        productDetails["Product Company"]=dataDictionary.get('pdpData').get('brand').get('name') 
    except Exception as err:
        productDetails["Product Company"]="None"
    try:
        productDetails["Product Name"]=dataDictionary.get('pdpData').get('name')
    except Exception as err:
        productDetails["Product Name"]="None"
    try:
        productDetails["Product ID"]=dataDictionary.get('pdpData').get('id') 
    except Exception as err:
        productDetails["Product ID"]="None"
    try:
        productDetails["Product Supplier"]=dataDictionary.get('pdpData').get('manufacturer')
    except Exception as err:
        productDetails["Product Supplier"]="None"
    try:
        productDetails["Product Country of Origin"]=dataDictionary.get('pdpData').get('countryOfOrigin') 
    except Exception as err:
        productDetails["Product Country of Origin"]="None"
    try:
        productDetails["Product Price"]=((dataDictionary.get('pdpData').get('discounts')[0].get('discountPercent')*dataDictionary.get('pdpData').get('mrp'))/100) 
    except Exception as err:
        productDetails["Product Price"]="None"
    try:
        productDetails["Product MRP"]=dataDictionary.get('pdpData').get('mrp')
    except Exception as err:
        productDetails["Product MRP"]="None"
    try:
        productDetails["Product Average Ratings"]=dataDictionary.get('pdpData').get('ratings').get('averageRating')
    except Exception as err:
        productDetails["Product Average Ratings"]="None"
    try:
        productDetails["Product Rating Count"]=dataDictionary.get('pdpData').get('ratings').get('totalCount') 
    except Exception as err:
        productDetails["Product Rating Count"]="None"
    try:
        productDetails["Product Gender"]=dataDictionary.get('pdpData').get('analytics').get('gender')
    except Exception as err:
        productDetails["Product Gender"]="None"
    return productDetails
def getProductData(url,category,fetchIndex):
    try:
        productDetails={}
        tempString=""
        res=requests.get(url)
        soup=BeautifulSoup(res.content.decode('utf-8','ignore'),"html.parser")
        try:
            for i in soup.find_all('script'):
                if str(i).find("window.__myx = ")!=-1:
                    dataDictionary=json.loads(str(i).replace("<script>","").replace("</script>","").replace("window.__myx = ",""))
        except Exception as err:
            print("ERROR: getProductData --> Check the data for script tag")
            print(err)
        try:
            productDetails=validationCheck(dataDictionary)
            productDetails["Product Category"]=category
        except Exception as err:
            print("ERROR: getProductData --> validationCheck() call")
            print(err)
        
        try:
            #Product Desciption
            tempString='"'
            for i in dataDictionary['pdpData']['productDetails']:
                tempString+=f"{i['title']}:{i['description']}-----"
            tempString+='"'
        except Exception as err:
            print("ERROR: getProductData --> Product Description")
            print(err)
        productDetails["Product Description"]=tempString
        lck.acquire()
        dataSet=pd.DataFrame(productDetails,index=[fetchIndex])
        dataSet.to_csv('dataSetTemp.csv',mode='a',header=False)
        lck.release()
    except Exception as err:
        print("ERROR: getProductData --> level 1")
        print(err)
    return
def deployPage(urls,category):
    with ThreadPoolExecutor(max_workers=50) as executor:
        for url in urls:
            try:
                executor.submit(getProductData,url,category,urls.index(url))
            except Exception as err:
                print("Error: deployPage")
                print(err)
    return
if __name__=="__main__":
    lck = threading.Lock()
    counter=0
    cateogoryData=pd.read_csv('listOfTypes.csv')
    for category in cateogoryData.iloc[:,[1,2]].values:
    #Point to be Noted: category[0] suggests name and category[1] suggests link to category
        baseUrl="https://www.myntra.com/"
        link=category[1]+"?p="
        currentPage=1
        urls=[]
        driver.get(link+str(1))
        content = driver.page_source
        soup=BeautifulSoup(content,"html.parser")
        pageCount=int(filterPageNumber(soup.find('li',class_="pagination-paginationMeta").text))
        print("Page Count: ",str(pageCount))
        with ThreadPoolExecutor(max_workers=15) as executorPage:
            for currPage in range(1,pageCount+1):
                if currPage > 4:
                    exit()
                driver.get(link+str(currPage))
                content = driver.page_source
                soup=BeautifulSoup(content,"html.parser")
                for i in soup.find_all('a',target="_blank"):
                    urls.append(baseUrl+i['href'])
                # print(urls)
                try:
                    future = executorPage.submit(deployPage,urls,category[0])
                except Exception as err:
                    logging.error(err)
                urls=[]
    print(counter)
    driver.close()
    driver.quit()
        