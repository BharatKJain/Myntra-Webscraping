from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import json
driver = webdriver.Chrome("C:/chromedriver")
# headers={
#     "Host": "www.myntra.com",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Referer": "https://www.myntra.com/men-tshirts",
#     "DNT": "1",
#     "Upgrade-Insecure-Requests": "1",
#     "Connection": "keep-alive",
#     "Cookie": "ak_bmsc=05C32415309D3406B3E93D5022ADFA9D170F21E5987F0000DB4DCB5EAB309153~plzVkJhoZKUILQLWLuW0Dx1aQE8ZZuaHn5DTzKwNjsc8TsbZFTpPi5QW2qDO0gAFHaxHoAY3TRyGjd/jt2kzQaEBeDu99nuzOFAqY9EinOQ60Z+ccvjAS5wg+qSQQO536flou4YtgOkiXvF2L65XUklu/KFXXzopxhwFH8cIruKMoesk3LJioi+71dM4FwCzdp6omIQgVtG6g46m/Pu8dS9FF+5VzcPG0LoRgDaWkOUqlMs8YCWbnLd8cj5V1FOR8t; akaas_myntra_SegmentationLabel=1592980149~rv=6~id=23fa6fb4c41bdce4d0c722520ff7cb7b~rn=PWA; bm_sz=71178D621BCF4248321AC429F2DDC743~YAAQ5SEPF8Jc5TJyAQAAcCAoSgeq0Ej1Ekg2mcdVA9TJjV5ujNi13Mwtqp+cAiiEZ/b9myW+sJD1w3n3REyEKVwJZGJdPna2fCmg+eINhFhICMQvpp/Xqy7sY7Q/q9tpKfjy4l3xByDGKjwJ2vIIz4rxn9naBLoB0VCpglJuSSNOFV9OYdtfY5NP8YECeh+g; _abck=EBF8F0C02266D4D9648BB0DBC2C9727C~0~YAAQdPAoFyfoxzFyAQAA+otPSgNtHKVl0E5OpbEoCxxygjlcR2MHAfXFHuoKqwGl0jbpxtLgqbShAx9eL3Ns2r7M1X8n/IaHXqrubysSw6t/ptzD+JWxBxGDKRV4z1c2O10Z02/+zt1bV/tsw7/dVwUNOITCmNyzNmhKHs1qsfoRTB9LgIj+CTY2UMb0XrrniWoeQ6Rqm9HK/R/R5ILzjIcyZS5yxHtnh0D+sJauMGZ9WMwQeVP4DIgAD8yXeQZBTHKhaVGGZAL2BaIceUFPWbO6TBlSmK/eqXDf/rwPAy4HIoTlq9NLwEVkHSqN0/TLtUmnK8KWgg==~-1~-1~-1; _d_id=2271cb30-4248-48b4-b8f4-3a2aa1af8f69; mynt-eupv=1; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWkRReFl6Y3dNRFV0T1dVME1pMHhNV1ZoTFRnME5HVXRNREF3WkROaFpqSTRaVE5tSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUyTURVNU16UXdORFVzSW1semN5STZJa2xFUlVFaWZRLlVIaWVQV0VodDlFMUI3UjNWa1hLc0JvVllzSG05T2M4ajBOT2ljdHdPVkE=; bc=true; xid=d41c7005-9e42-11ea-844e-000d3af28e3f; utm_track_1=a%3A7%3A%7Bs%3A10%3A%22utm_source%22%3Bs%3A6%3A%22direct%22%3Bs%3A10%3A%22utm_medium%22%3Bs%3A6%3A%22direct%22%3Bs%3A12%3A%22utm_campaign%22%3BN%3Bs%3A11%3A%22campaign_id%22%3BN%3Bs%3A12%3A%22octane_email%22%3BN%3Bs%3A10%3A%22trackstart%22%3Bi%3A1590382045%3Bs%3A8%3A%22trackend%22%3Bi%3A1590986845%3B%7D; utrid=a0UaXWt9UGYKbFofZ3FAMCM1NDg3MDY5NjMkMg%3D%3D.a216498b0be92d8ef37c37a73f79608b; _xsrf=7tvDP5zKpmtf58cuSC7VSxH3rDKBSsoI; bm_sv=20EF2EEDEAFC9C91B8EBCDAC83568CD0~JLCzpM+XJ9KbmI4CcazdSjs9LHwds8CFlHEpaI4wrw4tMpuNU5KWg40PnEeueU8FeCCbJ9HGThnz6pLgMwiFoIIrE8uDhS9YRFytYXvfpfL1qyZ7ioo7gdLCCTOSiEqTb8D3zBpu+3BDsIkiH7NskuHRcFH9r7N12O4/sHgUWF4=; _gcl_au=1.1.407447194.1590382045; _mxab_=config.bucket%3Dregular%3Bweb.xceleratorTags%3Denabled%3Bcheckout.cartmerge%3Denabled%3Btest-mobile-signup-newest%3DVariantA%3Bmobileonlylogin.recoverysetupsignup%3Dnotmandatory; lt_timeout=1; lt_session=1; AKA_A2=A; microsessid=830; dp=d; user_session=W3Q_wowkwPIag1UKG1mSSA.Q2GHltrY1wQldLpL76wqOw8nJZl6ixCoArjTG3labDBkRTsXQPfg4vRM4UzJXViAMw_vCBHqSdORU7oignplN5YGeLvZvuW1lAHOe8INfft8g1DNvWW5OXkFQ3TYJKS83uqTX1FF99Ocu8ad0aujiA.1590388126317.86400000.dWmnTlQopwY1VOirpj94qVXfFgipeLssNy-YwcjepgM",
#     "If-None-Match": 'W/"39516-NetVp3OWgS6zl4OrsNFYOwGs6/U"',
#     "Cache-Control": 'max-age=0',
#     "TE": 'Trailers'
# }
def filterPrice(string):
    return string[4:]
# def filterDiscount(string):
if __name__=="__main__":
    link="https://www.myntra.com/flip-flops/nike/nike-men-black-solid-thong-flip-flops/9082809/buy"
    driver.get(link)
    content = driver.page_source
    soup=BeautifulSoup(content,"html.parser")
    countForSupplier=0
    tempString=""
    productDetails={}
    tempDict={}
    productDescription={}
    
    for y in soup.findAll('div',attrs={'class':'pdp-description-container'}):
        #Name of Company of Product
        productDetails["Product Company Name: "]= (y.find('div',attrs={'class':'pdp-price-info'})).find('h1',attrs={'class':'pdp-title'}).text
        
        #Name of product
        productDetails["Product Name: "]=(y.find('div',attrs={'class':'pdp-price-info'})).find('h1',attrs={'class':'pdp-name'}).text
        
        #MRP and Price Information
        if (y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-mrp'}) is not None:
            productDetails["Product MRP: "]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-mrp'}).text[4:]
            productDetails["Product Price: "]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]
        else:
            productDetails["Product MRP: "]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]
            productDetails["Product Price: "]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-price'}).text[4:]         
        
        #Dicount Information
        if (y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-discount'}) is not None:
            productDetails["Dicount Information"]=(y.find('div',attrs={'class':'pdp-price-info'})).find('p',attrs={'class':'pdp-discount-container'}).find('span',attrs={'class':'pdp-discount'}).text
        else:
            productDetails["Dicount Information"]="0"

        #Product Information
        for i in (y.find('div',attrs={"class":"pdp-productDescriptors"})).find('div',attrs={'class':'pdp-productDescriptorsContainer'}).findAll('div'):
           if i.find('h4') is not None:
                # print(i.find('h4').text)
                if i.find('p') is not None:
                    productDetails[i.find('h4').text]=i.find('p').text
                else:
                    # print("Class of the calue: ",i.get('class'))
                    if i.get('class')[0]=='index-sizeFitDesc':
                        try:
                           element=driver.find_element_by_class_name("index-showMoreText")
                        except:
                            element=None 
                        
                        if element is not None:
                            # print("Inside")
                            retval=webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
                            elements=driver.find_elements_by_class_name("index-row")
                            tempString='"'
                            for element in elements:
                                tempString+=element.find_element_by_class_name("index-rowKey").text+':'+element.find_element_by_class_name("index-rowValue").text+','
                            tempString+='"'
                            productDetails[i.find('h4').text]=tempString
                            # print(tempString)
                            tempString=""
                        else:
                            elements=driver.find_elements_by_class_name("index-row")
                            tempString='"'
                            for element in elements:
                                tempString+=element.find_element_by_class_name("index-rowKey").text+':'+element.find_element_by_class_name("index-rowValue").text+','
                            tempString+='"'
                            productDetails[i.find('h4').text]=tempString
                            # print(tempString)
                            tempString=""
                    else:    
                        productDetails[i.find('h4').text]=i.text
        # print(productDetails


        
        
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
                    element=driver.find_element_by_class_name("supplier-viewmore-link")
                    # element=driver.find_element_by_class_name("//div[@class='supplier-viewmore-link']")
                    # print(element)
                    retval=webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
                    # print(retval)
                    elements=driver.find_elements_by_class_name("supplier-manufacturer")
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
    # print(json.dumps(productDetails))
    dataSet=pd.DataFrame(productDetails,index=[0])
    dataSet.to_csv('dataSet.csv')
    # soup.findAll()
    # print(list1)
    driver.close()
    driver.quit()
    exit()


    
