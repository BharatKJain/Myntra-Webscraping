from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

if __name__=="__main__":
    link="https://www.myntra.com/tshirts/wrogn/wrogn-men-navy-blue--maroon-striped-slim-fit-round-neck-t-shirt/11363560/buy"
    res=requests.get(link)
    productDetails={}
    tempString=""
    soup=BeautifulSoup(res.content.decode('utf-8','ignore'),"html.parser")
    for i in soup.find_all('script'):
        if str(i).find("window.__myx = ")!=-1:
            dataDictionary=json.loads(str(i).replace("<script>","").replace("</script>","").replace("window.__myx = ",""))
    productDetails={
        "Product Company":dataDictionary['pdpData']['brand']['name'] or 0,
        "Product Name":dataDictionary['pdpData']['name'] or 0,
        "Product Category":"Tshirts",
        "Product ID":dataDictionary['pdpData']['id'] or 0,
        "Product Supplier":dataDictionary['pdpData']['manufacturer'] or 0,
        "Product Country of Origin":dataDictionary['pdpData']['countryOfOrigin'] or 0,
        "Product Price":((dataDictionary['pdpData']['discounts'][0]['discountPercent']*dataDictionary['pdpData']['mrp'])/100) or 0,
        "Product MRP":dataDictionary['pdpData']['mrp'] or 0,
        "Product Discount":dataDictionary['pdpData']['discounts'][0]['label'] or 0,
        # "Product Description":str(dataDictionary['pdpData']['productDetails']) or 0,
        "Product Average Ratings":dataDictionary['pdpData']['ratings']['averageRating'] or 0,
        "Product Rating Count":dataDictionary['pdpData']['ratings']['totalCount'] or 0,
        "Product Gender":dataDictionary['pdpData']['analytics']['gender'] or 0
    }
    #Product Desciption
    tempString='"'
    for i in dataDictionary['pdpData']['productDetails']:
       tempString+=f"{i['title']}:{i['description']}-----"
    tempString+='"'
    productDetails["Product Description"]=tempString or 0

    #Product Ratings
    # for i in range(1,6):
    #     if i in dataDictionary['pdpData']['ratings']['ratingInfo'][:]["rating"]:
    #         dataDictionary["Product Rating "+str(i)+" stars (count)"]=i["rating"]
    #     else:
    #         dataDictionary["Product Rating "+str(i)+" stars (count)"]=0
    print(productDetails)


    
