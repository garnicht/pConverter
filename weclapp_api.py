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
    content = {"articleNumber" : article_number,                    # required
               "name" : article_name,                               # required
               "articleCategoryId": "48583",                        # ID-48583 steht für Konfigurationen
               'articleType': 'SALES_BILL_OF_MATERIAL',             # Verkaufstückliste
               'billOfMaterialPartDeliveryPossible': True,          # Stücklistenteillieferung möglich
               'useSalesBillOfMaterialItemPrices': False,           # Unterpositionen mit Preisen für Verkauf
               'useSalesBillOfMaterialItemPricesForPurchase': True} # Unterpositionen mit Preisen für Einkauf
    
    re = requests.post(url=url,headers=headers,json=content)

    if re.status_code == 201:
        print(f"Artikel mit Artikelnummer {article_number} und Artikelname {article_name} erfolgreich erstellt")
    else:
        print(f"Fehler beim Erstellen von Artikel {article_number}")
        print("Status Code:", re.status_code, "Content:", re.content)


# further infos for next steps:


#   'salesBillOfMaterialItems': [{'id': '805694',
#     'version': '0',
#     'articleId': '82463',
#     'articleNumber': 'G.NG',
#     'createdDate': 1721119433142,
#     'lastModifiedDate': 1721119433141,
#     'positionNumber': 1,
#     'quantity': '24'},
#    {'id': '805695',
#     'version': '0',
#     'articleId': '111653',
#     'articleNumber': 'G.NG_PB',
#     'createdDate': 1721119433143,
#     'lastModifiedDate': 1721119433142,
#     'positionNumber': 2,
#     'quantity': '6'},
