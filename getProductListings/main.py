from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import json
import logging

driver = webdriver.Chrome("C:/chromedriver")
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
if __name__=="__main__":
    countryOfOrigin=""
    baseUrl="https://www.myntra.com"
    link="https://www.myntra.com/men-tshirts?p="
    currentPage=1
    driver.get(link+str(currentPage))
    content = driver.page_source
    soup=BeautifulSoup(content,"html.parser")
    counter=0
    pageCount=int(filterPageNumber(soup.find('li',class_="pagination-paginationMeta").text))
    print("Page Count: ",str(pageCount))
    for i in soup.find_all('a',target="_blank"):
        print(i['href'])
        counter+=1
    print(counter)
    driver.close()
    driver.quit()
        