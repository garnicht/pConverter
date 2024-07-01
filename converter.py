#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


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


# In[3]:


# transform csv to df

encoding = detect_encoding("import.csv")

try:
    artikelliste_df = pd.read_csv("import.csv", sep=";", encoding=encoding)
except Exception as e:
    print(e)


# In[4]:


# get rid of empty Strings
artikelliste_df = artikelliste_df.apply(lambda x: x.replace("", None))


# In[5]:


artikelliste_df = artikelliste_df.query("Pos.notnull()")


# In[6]:


# gourp by Bezeichnung aka Artikelnummer to cumulate dublicates and get rid of NaN rows
artikelliste_df = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()


# In[7]:


# handle the columns we need / don't need
try: 
    artikelliste_df.insert(0,"Kopfartikelnummer",np.nan)
    artikelliste_df.insert(1,"platzhalter1",np.nan)
    artikelliste_df.insert(2,"platzhalter2",np.nan)
    artikelliste_df.insert(3,"platzhalter3",np.nan)
    artikelliste_df.insert(4,"platzhalter4",np.nan)
    artikelliste_df.insert(5,"platzhalter5",np.nan)
except Exception as e:
    print(e)


# In[8]:


#change name of existing columns
try:
    artikelliste_df.rename(columns={"Bezeichnung":"Artikelnummer","Menge":"Anzahl"},inplace=True)
except Exception as e:
    print(e)


# In[9]:


# ask for input and insert into df
artikelnummer = input("Wie lautet die Kopfartikelnummer?:")
artikelliste_df["Kopfartikelnummer"] = artikelnummer


# In[10]:


# get rid of dublicates
if not artikelliste_df[artikelliste_df["Artikelnummer"].duplicated()].empty:
    artikelliste_df = artikelliste_df[artikelliste_df["Artikelnummer"].duplicated(keep=False)]


# In[11]:


artikelliste_df.to_csv(f"finished_{artikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")

