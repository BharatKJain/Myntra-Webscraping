import pandas as pd 
cateogoryData=pd.read_csv('listOfTypes.csv')
for category in cateogoryData.iloc[:,[1,2]].values:
    print(category[0])