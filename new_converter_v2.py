#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
from weclapp_api_v2 import create_article, get_article_id
import re


# In[ ]:


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


# In[ ]:


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


# In[ ]:


def get_grid_type_and_colour(df_grouped):
    dummy = df_grouped[df_grouped["articleNumber"].str.startswith(("G.", "GF"))]
    
    typ = dummy.iloc[0]["articleNumber"].split(".")[0]

    if dummy.iloc[0]["articleNumber"].split(".")[1] == "NRB":    # hier zu NRB geändert
        colour = "NRB"
    elif dummy.iloc[0]["articleNumber"].split(".")[1] == "NG":
        colour = "NG"
    elif dummy.iloc[0]["articleNumber"].split(".")[1] == "NW":
        colour = "NW"
    
    else:
        print("coudn't recognize colour")
    
    return typ,colour


# In[ ]:


def solve_sm4_case():
    # test SM4
    if not artikelliste_df_grouped[artikelliste_df_grouped["articleNumber"].str.startswith("SM4")].empty:
        
        grids_grouped = artikelliste_df_grouped[artikelliste_df_grouped["articleNumber"].str.startswith(("G.", "GF"))]
        
        # calc sm4 sum
        sm4_filter = artikelliste_df_grouped['articleNumber'].str.startswith('SM4')
        sm4_quantities = artikelliste_df_grouped.loc[sm4_filter, 'quantity']
        sm4_sum = sm4_quantities.sum()
        
        minimum_grid = sm4_sum * 2

        # test existing Grids and their colours 
        if artikelliste_df_grouped[artikelliste_df_grouped["articleNumber"].str.startswith(("G.", "GF"))].shape[0] > 1:
            print(f"The Cubes in {kopfartikelnummer} configuration do have different colours or are mixed with flame retardned and normal. The special case SM4 is gonna be ignored now. Be aware.")
        
        elif (grids_grouped["quantity"] < minimum_grid).any():                 
            print(f"Zu wenige Grids in {kopfartikelnummer}. The special case SM4 is gonna be ignored now. Be aware.")
        
        else:            
            # normale Grids minus 2 * sm4 sum
            artikelliste_df_grouped.loc[artikelliste_df_grouped["articleNumber"].str.startswith(("G.", "GF")), "quantity"] -= (2*sm4_sum)

            # spezielle Grid + 1 je nach farbe
            typ, colour = get_grid_type_and_colour(artikelliste_df_grouped)
            article_number = typ + "." + colour + "_SM4"
            artikelliste_df_grouped.loc[len(artikelliste_df_grouped)+1]  = {"kopfartikelnummer":kopfartikelnummer, "articleNumber":article_number , "quantity":sm4_sum}

            print(f"Anzahl der SM4 Schränke und prepared Grids in '{kopfartikelnummer}':",sm4_sum, f"\nAnzahl der reduzierten normalen Grids in '{kopfartikelnummer}':",minimum_grid)


# In[ ]:


def check_special_colours(df):
    try:
        
        if not df[df["OFML Variant Code"].str.contains("remixcollection|guestcollection|CollectionVeneer|CollectionColor",na=False)].empty:
            
            pattern = r'Colors=[a-z]+([0-9]{2,})'
            mask = df["OFML Variant Code"].str.contains("remixcollection|guestcollection|CollectionVeneer|CollectionColor", na=False)

            for idx, row in df[mask].iterrows():
                ofml_code = row["OFML Variant Code"]
                match = re.search(pattern, ofml_code)

                if match:
                    extracted_value = match.group(1)
                    
                    # special case because filz / felt does already have a number at the end
                    if df.at[idx,"Article No."].startswith("PF"):
                        df.at[idx,"Article No."] = str(row["Article No."]) + "_" + extracted_value
                        print(f"Reihe {idx} wird zu Sondervariante {df.at[idx,"Article No."]}")
                         
                    else:
                        df.at[idx,"Article No."] = str(row["Article No."]) + extracted_value
                        print(f"Reihe {idx} wird zu Sondervariante {df.at[idx,"Article No."]}")
                    
                else:
                    print(f"Index: {idx}, No match found")
    
    except Exception as e:
        print(f"An error occured in function 'check_special_colours()':{e}")


# # Script starts here

# In[ ]:


## for developing
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)
#pd.reset_option('display.max_columns')
#pd.reset_option('display.max_colwidth')


# In[ ]:


# create article in WC and create csv for wizard if needed

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
        
        check_special_colours(artikelliste_df)

        # query and group
        artikelliste_df_grouped = artikelliste_df.groupby("Article No.")["Quantity"].sum().reset_index()
        
        # handle columns
        artikelliste_df_grouped = handle_columns(artikelliste_df_grouped)
        
        # handle artikelnummer '0' & 'AP'
        artikelliste_df_grouped = artikelliste_df_grouped.query("articleNumber != '0' and articleNumber != 'AP' ")

        artikelliste_df_grouped["kopfartikelnummer"] = kopfartikelnummer

        # # solve special cases
        try:
            solve_sm4_case()

        except Exception as e:
            print(e)
        
        artikelliste_df_grouped["articleId"] = artikelliste_df_grouped["articleNumber"].apply(get_article_id)

        #create article in weclapp and upload Stückliste
        try:

            dics_to_upload = artikelliste_df_grouped[["articleId","quantity"]].to_dict(orient="records")
            article_number = kopfartikelnummer
            article_name = input(f"Wie lautet der Artikelname von {article_number}:")
            create_article(kopfartikelnummer, article_name, dics_to_upload)
        except Exception as e:
            print(f"Error with create_article function. Code: {e}")
        
        # # create finished csvs
        artikelliste_df_grouped.to_csv(f"finished_{kopfartikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")


# In[ ]:


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


# In[ ]:


input("\nPress Enter to finish the script")

