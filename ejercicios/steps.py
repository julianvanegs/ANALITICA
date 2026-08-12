import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\coder\Downloads\julian\MOCK_DATA.csv")





#shape of database for example (#rows, #columns)
print(df.shape)
#the type of the data like str, float, int
print(df.dtypes)
#count the missing data
print(df.isnull().sum())

#SECOND STEP STANDARDIZE
standardize = (df.columns.str.replace(' ' , '_')
                         .str.lower()
                         .str.strip()
                         )

print(standardize)
#percent of the missing data
missing = df.isnull().mean()*100
print(missing[missing>0].sort_values(ascending=False))
