# %%
import pandas as pd
import numpy as np
import os 

# %%
# transform csv to df
try:
    artikelliste_df = pd.read_csv("import.csv", sep=";")
except Exception as e:
    print(e)
artikelliste_df.head()

# %%
# gourp by Bezeichnung aka Artikelnummer to cumulate dublicates and get rid of NaN rows
artikelliste_df = artikelliste_df.groupby("Bezeichnung")["Menge"].sum().reset_index()

# %%
# handle the columns we need / don't need
try: 
    artikelliste_df.insert(0,"Kopfartikelnummer",np.nan)
    artikelliste_df.insert(1,"Parent article name",np.nan)
    artikelliste_df.insert(2,"Parent article description",np.nan)
    artikelliste_df.insert(4,"Article name",np.nan)
    artikelliste_df.insert(5,"Article description",np.nan)
    artikelliste_df.insert(7,"Position no.",np.nan)
except Exception as e:
    print(e) 
       
artikelliste_df

# %%
#change name of existing columns
try:
    artikelliste_df.rename(columns={"Bezeichnung":"Artikelnummer","Menge":"QUANTITY"},inplace=True)
except Exception as e:
    print(e)
    
artikelliste_df.head()

# %%
# ask for input and insert into df
artikelnummer = input("Wie lautet die Kopfartikelnummer?:")
artikelliste_df["Kopfartikelnummer"] = artikelnummer
artikelliste_df.head(10)

# %%
artikelnummer_dublicates_df = artikelliste_df[artikelliste_df["Artikelnummer"].duplicated(keep=False)]
artikelnummer_dublicates_df.head()

# %%
artikelliste_df.to_csv(f"finished_{artikelnummer}.csv", index=False, sep=";")


