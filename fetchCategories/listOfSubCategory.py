import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome("C:/chromedriver")

if __name__=="__main__":
    link="https://www.myntra.com/men-tshirts"
    driver.get(link)
    content = driver.page_source
    soup=BeautifulSoup(content,"html.parser")
    listData=[]
    counter=0
    elements=driver.find_elements_by_tag_name("a")
    for element in elements:
        if element.get_attribute('class') == "desktop-categoryLink":
            # print(element.text)
            listData.append([element.get_attribute('textContent'),element.get_attribute('href')])
    data=pd.DataFrame(listData,columns=["Type","Link"])
    data.to_csv('listOfTypes.csv')
    driver.quit()
    exit()
                