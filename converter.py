#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


def detect_encoding(file_path):
    # Try reading the file with different encodings
    encodings = ['utf-8', 'latin1', 'cp1252', 'windows-1252', 'ISO-8859-1']  # Add more encodings as necessary

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return encoding
        
        except UnicodeDecodeError:
            continue  # Try next encoding if current one fails

    # If all encodings fail
    raise ValueError("Could not determine the encoding of the CSV file")


# In[ ]:


# transform csv to df

encoding = detect_encoding("import.csv")

try:
    artikelliste_df = pd.read_csv("import.csv", sep=";", encoding=encoding)
except Exception as e:
    print(e)


# In[ ]:


# get rid of empty Strings
artikelliste_df = artikelliste_df.apply(lambda x: x.replace("", None))


# In[ ]:


artikelliste_df = artikelliste_df.query("Pos.notnull()")


# In[ ]:


# gourp by Bezeichnung aka Artikelnummer to cumulate dublicates and get rid of NaN rows
artikelliste_df = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()


# In[ ]:


# handle the columns we need / don't need
try: 
    artikelliste_df.insert(0,"Kopfartikelnummer",np.nan)
    artikelliste_df.insert(1,"Kopfartikelname",np.nan)
    artikelliste_df.insert(2,"Kopfartikelbeschreibung",np.nan)
    artikelliste_df.insert(3,"Artikelname",np.nan)
    artikelliste_df.insert(4,"Artikelbeschreibung	",np.nan)
    artikelliste_df.insert(5,"Positionsnummer",np.nan)
except Exception as e:
    print(e)


# In[ ]:


#change name of existing columns
try:
    artikelliste_df.rename(columns={"Bezeichnung":"Artikelnummer","Menge":"Anzahl"},inplace=True)
except Exception as e:
    print(e)


# In[ ]:


# ask for input and insert into df
artikelnummer = input("Wie lautet die Kopfartikelnummer?:")
artikelliste_df["Kopfartikelnummer"] = artikelnummer


# In[ ]:


# get rid of dublicates
if not artikelliste_df[artikelliste_df["Artikelnummer"].duplicated()].empty:
    artikelliste_df = artikelliste_df[artikelliste_df["Artikelnummer"].duplicated(keep=False)]


# In[ ]:


artikelliste_df.to_csv(f"finished_{artikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")

