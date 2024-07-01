#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# transform csv to df
try:
    artikelliste_df = pd.read_csv("import.csv", sep=";")
except Exception as e:
    print(e)


# In[3]:


# get rid of empty Strings
artikelliste_df = artikelliste_df.apply(lambda x: x.replace("", None))


# In[4]:


artikelliste_df = artikelliste_df.query("Pos.notnull()")


# In[5]:


# gourp by Bezeichnung aka Artikelnummer to cumulate dublicates and get rid of NaN rows
artikelliste_df = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()


# In[6]:


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


# In[7]:


#change name of existing columns
try:
    artikelliste_df.rename(columns={"Bezeichnung":"Artikelnummer","Menge":"Anzahl"},inplace=True)
except Exception as e:
    print(e)


# In[8]:


# ask for input and insert into df
artikelnummer = input("Wie lautet die Kopfartikelnummer?:")
artikelliste_df["Kopfartikelnummer"] = artikelnummer


# In[9]:


# get rid of dublicates
if not artikelliste_df[artikelliste_df["Artikelnummer"].duplicated()].empty:
    artikelliste_df = artikelliste_df[artikelliste_df["Artikelnummer"].duplicated(keep=False)]


# In[10]:


artikelliste_df.to_csv(f"finished_{artikelnummer}.csv", index=False, sep=";")

