from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import logging
import threading 
from concurrent.futures import ThreadPoolExecutor

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

def getProductData(url,category,fetchIndex):
    print("Inside Function")
    print("With URL: ",url)
    driver2=webdriver.Chrome("C:/chromedriver",options=chrome_options)
    driver2.get(url)
    content = driver2.page_source
    soup=BeautifulSoup(content,"html.parser")
    countForSupplier=0
    tempString=""
    productDetails={}
    tempDict={}
    productDescription={}

    productDetails['Category']=category
    
    for y in soup.findAll('div',attrs={'class':'pdp-description-container'}):
        #Name of Company of Product
        productDetails["Product Company Name"]='"'+(y.find('div',attrs={'class':'pdp-price-info'})).find('h1',attrs={'class':'pdp-title'}).text+'"'
        
        #Name of product
        productDetails["Product Name"]='"'+(y.find('div',attrs={'class':'pdp-price-info'})).find('h1',attrs={'class':'pdp-name'}).text+'"'
        
        #MRP and Price Information
        if (y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-mrp'}) is not None:
            productDetails["Product MRP"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-mrp'}).text[4:]
            productDetails["Product Price"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]
        else:
            productDetails["Product MRP"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]
            productDetails["Product Price"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]         
        
        #Dicount Information
        if (y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-discount'}) is not None:
            productDetails["Dicount Information"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-discount'}).text
        else:
            productDetails["Dicount Information"]="0"

        # Product Information
        for i in (y.find('div',attrs={"class":"pdp-productDescriptors"})).find('div',attrs={'class':'pdp-productDescriptorsContainer'}).findAll('div'):
           if i.find('h4') is not None:
                # print(i.find('h4').text)
                if i.find('p') is not None:
                    productDescription[i.find('h4').text]='"'+i.find('p').text+'"'
                else:
                    # print("Class of the calue: ",i.get('class'))
                    if i.get('class')[0]=='index-sizeFitDesc':
                        try:
                           element=driver2.find_element_by_class_name("index-showMoreText")
                        except:
                            element=None 
                        
                        if element is not None:
                            # print("Inside")
                            retval=webdriver.ActionChains(driver2).move_to_element(element).click(element).perform()
                            elements=driver2.find_elements_by_class_name("index-row")
                            tempString='"'
                            for element in elements:
                                tempString+=element.find_element_by_class_name("index-rowKey").text+':'+element.find_element_by_class_name("index-rowValue").text+','
                            tempString+='"'
                            productDescription[i.find('h4').text]='"'+tempString+'"'
                            # print(tempString)
                            tempString=""
                        else:
                            elements=driver2.find_elements_by_class_name("index-row")
                            tempString='"'
                            for element in elements:
                                tempString+=element.find_element_by_class_name("index-rowKey").text+':'+element.find_element_by_class_name("index-rowValue").text+','
                            tempString+='"'
                            productDescription[i.find('h4').text]='"'+tempString+'"'
                            # print(tempString)
                            tempString=""
                    else:    
                        productDescription[i.find('h4').text]='"'+i.text+'"'
        # print(productDescription)
        productDetails["Product Details "]='"'+str(productDescription)+'"'


        
        
        #Data for Supplier information
        for i in y.findAll('div',attrs={'class':'undefined supplier-desktopCodeSupplier'}):
            for j in i.findAll('div'):
                if countForSupplier==0:
                    productDetails["Product Code"]=j.find('span',attrs={"class":"supplier-styleId"}).text
                elif countForSupplier==1:
                    for k in j.findAll('span'):
                        tempString+=k.text
                        # print(k.text)
                    productDetails["Seller Information"]=tempString
                    tempString=""
                else:
                    element=driver2.find_element_by_class_name("supplier-viewmore-link")
                    # element=driver2.find_element_by_class_name("//div[@class='supplier-viewmore-link']")
                    # print(element)
                    retval=webdriver.ActionChains(driver2).move_to_element(element).click(element).perform()
                    # print(retval)
                    elements=driver2.find_elements_by_class_name("supplier-manufacturer")
                    # print(j)
                    tempString='"'
                    for el in elements:
                        # print(element.text)
                        for element in el.find_elements_by_tag_name('div'):
                            if element.get_attribute('class') == "supplier-met-values":
                                tempString+=element.text
                            else:
                                tempString+=element.text+"::"
                        tempString+='-----'
                    tempString+='"'
                    productDetails["Source of Product"]=tempString
                    tempString=""
                countForSupplier+=1
    global lck
    dataSet=pd.DataFrame(productDetails,index=[fetchIndex])
    dataSet.to_csv('dataSetTemp.csv',mode='a',header=True)
    lck.release()
    driver2.close()
    driver2.quit()
    return
def deployPage(urls,category):
    print("Inside Deploy Page")
    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in urls:
            try:
                print("Here")
                print(url)
                future = executor.submit(getProductData,url,category,urls.index(url))
            except Exception as err:
                logging.error(err)
    print("Success in deployPage")
    return
if __name__=="__main__":
    lck = threading.Lock()
    counter=0
    cateogoryData=pd.read_csv('listOfTypes.csv')
    for category in cateogoryData.iloc[:,[1,2]].values:
    #Point to be Noted: category[0] suggests name and category[1] suggests link to category
        baseUrl="https://www.myntra.com/"
        link=category[1]+"?p="
        category=category[0]
        currentPage=1
        urls=[]
        driver.get(link+str(1))
        content = driver.page_source
        soup=BeautifulSoup(content,"html.parser")
        pageCount=int(filterPageNumber(soup.find('li',class_="pagination-paginationMeta").text))
        print("Page Count: ",str(pageCount))
        with ThreadPoolExecutor(max_workers=3) as executorPage:
            for currPage in range(1,pageCount+1):
                driver.get(link+str(currPage))
                content = driver.page_source
                soup=BeautifulSoup(content,"html.parser")
                for i in soup.find_all('a',target="_blank"):
                    urls.append(baseUrl+i['href'])
                print(urls)
                try:
                    future = executorPage.submit(deployPage,urls,category[0])
                except Exception as err:
                    logging.error(err)
                urls=[]
    print(counter)
    driver.close()
    driver.quit()
        