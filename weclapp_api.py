#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
from dotenv import load_dotenv


# In[ ]:


load_dotenv()


# In[ ]:


def create_article(article_number, article_name):
    url = "https://degridstudio.weclapp.com/webapp/api/v1/article"
    token = os.getenv("weclapp_token")
    headers = {"AuthenticationToken" : token,
               "Content-Type" : "application/json"}
    content = {"articleNumber" : article_number,
               "name" : article_name,
               "articleCategoryId": "48583",
               'articleType': 'SALES_BILL_OF_MATERIAL',
               'availableForSalesChannels': [],
               'availableInSale': True,
               'batchNumberRequired': False,
               'billOfMaterialPartDeliveryPossible': True,}
    
    re = requests.post(url=url,headers=headers,json=content)

    if re.status_code == 201:
        print(f"Artikel mit Artikelnummer {article_number} und Name {article_name} erfolgreich erstellt")
    else:
        print(f"Fehler beim Erstellen von Artikel {article_number}")
        print("Status Code:", re.status_code, "Content:", re.content)

