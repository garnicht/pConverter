#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import os


# In[6]:


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


# In[7]:


def handle_columns(df):
    
    try: 
        df.insert(0,"Kopfartikelnummer",np.nan)
        df.insert(1,"Kopfartikelname",np.nan)
        df.insert(2,"Kopfartikelbeschreibung",np.nan)
        df.insert(3,"Artikelname",np.nan)
        df.insert(4,"Artikelbeschreibung",np.nan)
        df.insert(5,"Positionsnummer",np.nan)
        df.rename(columns={"Bezeichnung":"Artikelnummer","Menge":"Anzahl"},inplace=True)
    except Exception as e:
        print(e)


# In[8]:


# loop through csvs, insert /delete the right columns and insert kopfartikelnummer

for file in os.listdir():
    if file.endswith(".csv"):
        
        kopfartikelnummer = file.split(".")[0]
        encoding = detect_encoding(file)
        
        try:
            artikelliste_df = pd.read_csv(file, sep=";", encoding=encoding)
        except Exception as e:
            print(e)
        
        # get rid of empty Strings
        artikelliste_df = artikelliste_df.apply(lambda x: x.replace("", None))
        
        #query and group
        artikelliste_df.query("Pos.notnull()", inplace=True)
        artikelliste_df_grouped = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()
        
        handle_columns(artikelliste_df_grouped)
        
        artikelliste_df_grouped["Kopfartikelnummer"] = kopfartikelnummer

        artikelliste_df_grouped.to_csv(f"finished_{kopfartikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")

