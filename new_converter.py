#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from weclapp_api import create_article, get_recent_articles


# In[2]:


def detect_encoding(file_path):
    # Try reading the file with different encodings
    encodings = ['utf-8', 'latin1', 'cp1252', 'windows-1252', 'ISO-8859-1']  # Add more encodings as necessary

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, sep=";")
            return encoding
        
        except UnicodeDecodeError:
            continue  # Try next encoding if current one fails

    # If all encodings fail
    raise ValueError("Could not determine the encoding of the CSV file")


# In[3]:


def handle_columns(df):
    columns_to_keep = ["article_no.","quantity"]
    
    try: 
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df = df.loc[:,columns_to_keep]
        df.insert(0,"kopfartikelnummer",np.nan)
        df.insert(1,"kopfartikelname",np.nan)
        df.insert(2,"kopfartikelbeschreibung",np.nan)
        df.insert(3,"artikelname",np.nan)
        df.insert(4,"artikelbeschreibung",np.nan)
        df.insert(5,"positionsnummer",np.nan)
        df.rename(columns={"article_no.":"articleNumber"},inplace=True)

        return df

    except Exception as e:
        print(e)


# In[4]:


def get_grid_type_and_colour(df_grouped):
    dummy = df_grouped[df_grouped["Artikelnummer"].str.startswith(("G.", "GF"))]
    
    typ = dummy.iloc[0]["Artikelnummer"].split(".")[0]

    if dummy.iloc[0]["Artikelnummer"].split(".")[1] == "NB":
        colour = "NB"
    elif dummy.iloc[0]["Artikelnummer"].split(".")[1] == "NG":
        colour = "NG"
    elif dummy.iloc[0]["Artikelnummer"].split(".")[1] == "NW":
        colour = "NW"
    
    else:
        print("coudn't recognize colour")
    
    return typ,colour


# In[5]:


def solve_sm4_case():
    # test SM4
    if not artikelliste_df_grouped[artikelliste_df_grouped["Artikelnummer"].str.startswith("SM4")].empty:
        
        dummy_grouped = artikelliste_df_grouped[artikelliste_df_grouped["Artikelnummer"].str.startswith(("G.", "GF"))]

        # test existing Grids and their colours 
        if artikelliste_df_grouped[artikelliste_df_grouped["Artikelnummer"].str.startswith(("G.", "GF"))].shape[0] > 1:
            print("The Cubes in this configuration do have different colours or are mixed with flame retardned and normal. The special case about SM4 cannot be solved now. Be aware.")
        
        elif (dummy_grouped["Anzahl"] <=2).any():
            print("Zu wenige Grids in Liste. SM4 cant be solved. Be aware!")
        
        else: 

            # normale Grids minus 2 
            artikelliste_df_grouped.loc[artikelliste_df_grouped["Artikelnummer"].str.startswith(("G.", "GF")), "Anzahl"] -= 2

            # spezielle Grid + 1 je nach farbe
            typ, colour = get_grid_type_and_colour(artikelliste_df_grouped)
            artikelnummer = typ + "." + colour + "_SM4"
            artikelliste_df_grouped.loc[len(artikelliste_df_grouped)]  = {"Kopfartikelnummer":kopfartikelnummer, "Artikelnummer":artikelnummer , "Anzahl":1}


# In[6]:


# create csv for upload

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
        
        # query and group
        artikelliste_df_grouped = artikelliste_df.groupby("Article No.")["Quantity"].sum().reset_index()
        
        # handle columns
        artikelliste_df_grouped = handle_columns(artikelliste_df_grouped)
        
        # handle '0' artikelnummer
        artikelliste_df_grouped = artikelliste_df_grouped.query("articleNumber != '0'")

        artikelliste_df_grouped["kopfartikelnummer"] = kopfartikelnummer

        # # solve special cases
        # try:
        #     solve_sm4_case()

        # except Exception as e:
        #     print(e)
        
        #create article in weclapp and upload Stückliste
        try:
            dics_to_upload = artikelliste_df_grouped[["articleNumber","quantity"]].to_dict(orient="records")
            article_number = kopfartikelnummer
            article_name = input(f"Wie lautet der Artikelname von {article_number}:")
            create_article(kopfartikelnummer, article_name, dics_to_upload)
        except Exception as e:
            print(f"Error with create_article function. Code: {e}")
        
        # create finished csvs
        artikelliste_df_grouped.to_csv(f"finished_{kopfartikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")


# In[7]:


# prototyp um converter movable zu machen
# # create csv for upload

# working_directory = os.getcwd()
# path_to_dir_with_csv = os.path.join(working_directory,"..")

# for file in os.listdir(os.getcwd()):
#     if file.endswith(".csv"):
#         path_to_file = os.path.join(path_to_dir_with_csv,file)
#         kopfartikelnummer = path_to_file.split(".")[0]
#         encoding = detect_encoding(path_to_file)
        
#         try:
#             artikelliste_df = pd.read_csv(path_to_file, sep=";", encoding=encoding)
#         except Exception as e:
#             print(e)
        
#         # get rid of empty Strings
#         artikelliste_df = artikelliste_df.apply(lambda x: x.replace("", None))
        
#         #query and group
#         artikelliste_df.query("Pos.notnull()", inplace=True)
#         artikelliste_df_grouped = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()
        
#         handle_columns(artikelliste_df_grouped)
        
#         artikelliste_df_grouped["Kopfartikelnummer"] = kopfartikelnummer

#         # solve special cases
#         try:
#             solve_sm4_case()

#         except Exception as e:
#             print(e)
        
#         #create article in weclapp and upload Stückliste
#         try:
#             artikelliste_df_grouped.rename(inplace=True, columns={"Artikelnummer":"articleNumber", "Anzahl":"quantity"})
#             dics_to_upload = artikelliste_df_grouped[["articleNumber","quantity"]].to_dict(orient="records")
#             article_number = kopfartikelnummer
#             article_name = input(f"Wie lautet der Artikelname von {article_number}:")
#             create_article(kopfartikelnummer, article_name, dics_to_upload)
#         except Exception as e:
#             print(f"Error with create_article function. Code: {e}")
        
#         # create finished csvs
#         artikelliste_df_grouped.to_csv(f"{path_to_dir_with_csv}/finished_{kopfartikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")


# In[8]:


input("Press Enter to finish the script")
