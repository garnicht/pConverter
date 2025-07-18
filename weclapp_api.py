#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
from dotenv import load_dotenv
from install_token import get_env_path


# In[ ]:

env_file_path = get_env_path()
load_dotenv(dotenv_path=env_file_path, override=True)


# In[ ]:

def create_article(article_number, article_name, dics_to_upload):
    url = "https://degridstudio.weclapp.com/webapp/api/v1/article"
    token = os.getenv("weclapp_token")
    headers = {"AuthenticationToken" : token,
               "Content-Type" : "application/json",
               "Accept-Encoding" : "gzip"}                          # ab update von 01.02. ist encoding pflicht
    content = {"articleNumber" : article_number,                    # required
               "name" : article_name,                               # required
               "articleCategoryId": "48583",                        # ID-48583 steht für Konfigurationen
               'articleType': 'SALES_BILL_OF_MATERIAL',             # Verkaufstückliste
               'billOfMaterialPartDeliveryPossible': True,          # Stücklistenteillieferung möglich
               'useSalesBillOfMaterialItemPrices': False,           # Unterpositionen mit Preisen für Verkauf
               'useSalesBillOfMaterialItemPricesForPurchase': True, # Unterpositionen mit Preisen für Einkauf
               'useSalesBillOfMaterialSubitemCosts': True,          # Unterpositionen mit Kosten im Verkauf 
               "salesBillOfMaterialItems" : dics_to_upload}         # Verkaufstückliste upload mit den einzelnen Artikeln input = articlename und quantity
    re = requests.post(url=url,headers=headers,json=content)

    if re.status_code == 201:
        print(f"Artikel mit Artikelnummer {article_number} und Artikelname {article_name} erfolgreich erstellt")
    elif re.json()["error"].startswith("article not found:"): # falls artikel von verkaufstückliste nich in WC (passiert wegen sonderfarben)
        print("ERROR:", re.json()["error"] , "---> Erstelle diesen Artikel manuell in WC, lösche die finished_csv und starte den converter von neuem.")
    else:
        print(f"Fehler beim Erstellen von Artikel {article_number}")
        print("Status Code:", re.status_code, "Content:", re.content)
    return re

def get_recent_articles():
    url = "https://degridstudio.weclapp.com/webapp/api/v1/article?sort=-lastModifiedDate"
    token = os.getenv("weclapp_token")
    headers = {"AuthenticationToken" : token,
            "Content-Type" : "application/json"}
    re = requests.get(url=url, headers=headers)
    return re