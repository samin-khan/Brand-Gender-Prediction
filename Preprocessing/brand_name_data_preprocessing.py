import pandas as pd
import numpy as np
import operator
from openpyxl import load_workbook
import re

# Name of raw data file to read from. Assuming there is column 'Brand' and 'Category'
data_file = "brand_names.xlsx"
dfRaw = pd.read_excel(data_file)

# Makes all names lowercase
dfRaw['Brand'] = dfRaw['Brand'].str.lower()

# Open British National Corpus
lemma = open("lemma.al.txt", "r")
count = 0
word_list = []
for line in lemma.readlines():
    words = line.split(" ")
    if words[2].isalpha():
        word_list.append(words[2])

# Removes brand names based on real English words
for row in dfRaw.iterrows():
    if row[1][0] in word_list:
        dfRaw.drop(row[0], inplace=True)  

# Removes single letter names if any
dfRaw['isOneChar'] = dfRaw["Brand"].str.len() < 2
dfRaw = dfRaw.drop(dfRaw[dfRaw["isOneChar"] == True].index)
dfRaw = dfRaw.drop(['isOneChar'], axis=1)

# Removes multi-word and non-alphabetic brand names
i = 0
dfEmpty = dfRaw.iloc[0:0]
for row in dfRaw.itertuples():
    if len(row.words) == 1 and row.Brand.isalpha():
        dfEmpty.loc[i] = list(row)
        i += 1

"""Adding coding schemes"""
# Adding 16 features to dataframe
dfFeatures = dfEmpty
Name = 'Brand'

# A ending?
dfFeatures['A ending?'] = 0
dfFeatures.loc[(dfFeatures[Name].str.endswith('a', na=False)), 'A ending?'] = 1

# Plosive ending? (p,b,t,d,k,g)
dfFeatures["Plosive ending? (p,b,t,d,k,g)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.endswith('p', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('b', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('t', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('d', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('k', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('g', na=False)), "Plosive ending? (p,b,t,d,k,g)"] = 1

# Sonorant ending? (m,n,ng,l,r)
dfFeatures["Sonorant ending? (m,n,ng,l,r)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.endswith('m', na=False)), "Sonorant ending? (m,n,ng,l,r)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('n', na=False)), "Sonorant ending? (m,n,ng,l,r)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('ng', na=False)), "Sonorant ending? (m,n,ng,l,r)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('l', na=False)), "Sonorant ending? (m,n,ng,l,r)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('r', na=False)), "Sonorant ending? (m,n,ng,l,r)"] = 1

# Fricative ending? (f,v,th,s,z,sh,ch,dge)
dfFeatures["Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.endswith('f', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('v', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('th', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('s', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('z', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('sh', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('dge', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('ch', na=False)), "Fricative ending? (f,v,th,s,z,sh,ch,dge)"] = 1

# 1st letter fricative? (f,v,th,s,z,sh,ch,j)
dfFeatures["1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.startswith('f', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('v', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('th', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('s', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('z', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('sh', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('ch', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('j', na=False)), "1st letter fricative? (f,v,th,s,z,sh,ch,j)"] = 1

# Total # of sonorants (m,n,l,r,w,y)
dfFeatures["Total # of sonorants (m,n,l,r,w,y)"] = dfFeatures.Brand.str.count("[mnlrwy]")

# Total # of vowels (a, e, i, o, u)
dfFeatures["Total # of vowels (a, e, i, o, u)"] = dfFeatures.Brand.str.count("[aeiou]")

# 1st letter plosive? (p,b,t,d,k,g)
dfFeatures["1st letter plosive? (p,b,t,d,k,g)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.startswith('p', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('b', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('t', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('d', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('k', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith('g', na=False)), "1st letter plosive? (p,b,t,d,k,g)"] = 1

# Total # of plosives  (p,b,t,d,k,g)
dfFeatures["Total # of plosives  (p,b,t,d,k,g)"] = dfFeatures.Brand.str.count("[pbtdkg]")

# VowelEnding? (a, e, i, o, u,y)
dfFeatures["VowelEnding? (a, e, i, o, u,y)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.endswith('a', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('e', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('i', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('o', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('u', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.endswith('y', na=False)), "VowelEnding? (a, e, i, o, u,y)"] = 1

# # of letters
dfFeatures["# of letters"] = dfFeatures.Brand.str.len()

# Total # of fricatives (f,v,th,s,z,sh,ch,j)
dfFeatures["# of fricatives (f,v,th,s,z,sh,ch,j)"] = (dfFeatures.Brand.str.count("[fvzj]") + dfFeatures.Brand.str.count("(sh)|s") 
                                                      + dfFeatures.Brand.str.count("(th)") + dfFeatures.Brand.str.count("(ch)"))

# 1st letter vowel? (a, e, i, o, u)
dfFeatures["1st letter vowel? (a, e, i, o, u)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.startswith("a", na=False)), "1st letter vowel? (a, e, i, o, u)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("e", na=False)), "1st letter vowel? (a, e, i, o, u)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("i", na=False)), "1st letter vowel? (a, e, i, o, u)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("o", na=False)), "1st letter vowel? (a, e, i, o, u)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("u", na=False)), "1st letter vowel? (a, e, i, o, u)"] = 1

# 1st letter sonorant? (m,n,l,r,w,y)
dfFeatures["1st letter sonorant? (m,n,l,r,w,y)"] = 0
dfFeatures.loc[(dfFeatures[Name].str.startswith("m", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("n", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("l", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("r", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("w", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1
dfFeatures.loc[(dfFeatures[Name].str.startswith("y", na=False)), "1st letter sonorant? (m,n,l,r,w,y)"] = 1

def num_front_vowels(name: str) -> int:
    regex = re.compile(r"Ee|Ie|Ei|E|I|ee|ei|ie|e|i")
    y_ending = 1 if name.endswith('y') else 0
    return len(regex.findall(name)) + y_ending

def num_back_vowels(name: str) -> int:
    regex = re.compile(r"Oo|Ou|O|U|oo|ou|o|u")
    return len(regex.findall(name))

dfFeatures["Front Vowels"] = dfFeatures[Name].apply(num_front_vowels)
dfFeatures["Back Vowels"] = dfFeatures[Name].apply(num_back_vowels)

dfFeatures = dfFeatures.dropna()

dfFeatures.to_csv('brand_names_coded.csv')


