# %%
import pandas as pd
import numpy as np
import os
from weclapp_api import create_article

# %%
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

# %%
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

# %%
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

# %%
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

# %%
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
        
        #query and group
        artikelliste_df.query("Pos.notnull()", inplace=True)
        artikelliste_df_grouped = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()
        
        handle_columns(artikelliste_df_grouped)
        
        artikelliste_df_grouped["Kopfartikelnummer"] = kopfartikelnummer

        try:
            solve_sm4_case()

        except Exception as e:
            print(e)
        
        #create article in weclapp
        try:
            article_number = kopfartikelnummer
            article_name = input(f"Wie lautet der Artikelname von {article_number}:")
            create_article(kopfartikelnummer,article_name)
        except Exception as e:
            print(f"Error with create_article function. Code: {e}")
        
        # create finished csvs
        artikelliste_df_grouped.to_csv(f"finished_{kopfartikelnummer}.csv", index=False, sep=";", encoding="ISO-8859-1")

# %%
input("Press Enter to finish the script")


