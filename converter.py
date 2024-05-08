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
# create / delete  the columns we need / dont need
try: 
    artikelliste_df.drop(columns="Pos", inplace=True)
    artikelliste_df.insert(0,"PARENT ARTICLE NO.",np.nan)
    artikelliste_df.insert(1,"Parent article name",np.nan)
    artikelliste_df.insert(2,"Parent article description",np.nan)
    artikelliste_df.insert(4,"Article name",np.nan)
    artikelliste_df.insert(5,"Article description",np.nan)
    artikelliste_df.insert(7,"Position no.",np.nan)
except Exception as e:
    print(e) 
       
artikelliste_df.head()

# %%
#change name of existing columns
try:
    artikelliste_df.rename(columns={"Bezeichnung":"ARTICLE NO.","Menge":"QUANTITY"},inplace=True)
except Exception as e:
    print(e)
    
artikelliste_df.head()

# %%
# remove the redundant NaN rows
artikelliste_df = artikelliste_df[artikelliste_df["ARTICLE NO."].notna()]
artikelliste_df.head()

# %%
# ask for input and insert into df
artikelnummer = input("Wie lautet die Artikelnummer?:")
artikelliste_df["PARENT ARTICLE NO."] = artikelnummer
artikelliste_df.head()

# %%
# create new csv
if os.path.exists("finished.csv"):
    print("finished.csv gibt es bereits.")
    dateiname = input("Bitte Tippe einen neuen Namen für die Datei ein (Ohne '.csv'):")
    artikelliste_df.to_csv(f"{dateiname}.csv", index=False)

else:
    artikelliste_df.to_csv("finished.csv", index=False)


