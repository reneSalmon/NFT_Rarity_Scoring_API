## 01 Product vision and goals

#Vision
#An API that enables user to identify the most rar NFTs

#Goal 01: Create a Traits_rarity_score
#Goal 02: Create a NFT_rarity_score

## 02 Import moduls
import requests
import collections
import pandas as pd
from itertools import islice


## 03 Get Data via API
#Call OpenSea API to get CryptoTrunks Data
response = requests.get("https://api.opensea.io/api/v1/assets?collection=cryptotrunks&format=json&limit=50&offset=50&order_direction=desc")
print(response.status_code)

#Save first 50 CryptoTrunks Data as JSON
Crypto_trunks_50_json = response.json()
Crypto_trunks_50_json


## 04 Data preprocessing

#List of NFT_IDs
List_of_50_NFTs = Crypto_trunks_50_json['assets']
NFT_ID =[List_of_50_NFTs[NFT]['token_id']
          for NFT in range(len(Crypto_trunks_50_json['assets']))]

#Trait_types in JSON
List_of_Traits_in_all_NFTs = [
    List_of_50_NFTs[NFT]['traits']
    for NFT in range(len(Crypto_trunks_50_json['assets']))]
List_of_Traits_in_all_NFTs

print(len(List_of_Traits_in_all_NFTs))
print(List_of_Traits_in_all_NFTs[0])


## 05 Goal 01: Traits_Rarity_Score

# 1. Create Lists for the DataFrame

# Trait_types
#How to get the Trait_types for every NFT?
Trait_types_for_NFTs = [
    List_of_Traits_in_all_NFTs[NFT][TRAITE]['trait_type']
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]

#Trait_Values
#How to generate a value for every trait?
Trait_value_for_NFTs = [
    List_of_Traits_in_all_NFTs[NFT][TRAITE]['value']
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]

#Trait_counts
Trait_count_for_NFTs = [
    List_of_Traits_in_all_NFTs[NFT][TRAITE]['trait_count']
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]

#Percentages%
#Trait_type_rarity_percentages

Total_amount_of_crypto_trunks = 23.500 #PROBLEM!!!! Where do we fetch this number from?

Trait_rarity_percentage = [
    List_of_Traits_in_all_NFTs[NFT][TRAITE]['trait_count']/Total_amount_of_crypto_trunks
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]

#NFT_IDs
# How do I create a DataFrame where all NFT_IDs match with amount of Traits?
NFT_IDs_for_each_trait = [
    List_of_50_NFTs[NFT]['token_id']
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]

#Trait_rarity_score
# How to calculate a rarity_score for every trait?
Trait_rarity_score = [
    1/(List_of_Traits_in_all_NFTs[NFT][TRAITE]['trait_count']/Total_amount_of_crypto_trunks)
    for NFT in range(len(List_of_Traits_in_all_NFTs))
    for TRAITE in range(len(List_of_Traits_in_all_NFTs[NFT]))
    ]


# 2. Create DataSet and display it in a DataFrame

data = {'NFT_IDs': NFT_IDs_for_each_trait,
        'Trait_Types': Trait_types_for_NFTs,
        'Trait_Values': Trait_value_for_NFTs,
        'Trait_Counts': Trait_count_for_NFTs,
        'Type_Rarity_Percentages': Trait_rarity_percentage,
        'Trait_Rarity_Scores': Trait_rarity_score
        #'Trait_IDs': [1,2,3,4,5,1,2,3,1,2,3,4,] #Do it with pandas
        #'Ranking_position': [16.6, 8.6, 8.6, 12.5], #Do it with pandas
       }

df = pd.DataFrame.from_dict(data)

#Trait_IDs
df['Trait_Ids'] = df.groupby('NFT_IDs').cumcount() + 1

#Sort columns
col = df.pop("Trait_Ids")
df.insert(1, col.name, col)
df

#return df???

## 06 Goal 02: NFT_rarity_score

#Create List with all NFT_rarity scores
NFT_rarity_score = []


#Count all traits per NFT
count_of_traits_per_NFT = collections.Counter(NFT_IDs_for_each_trait)

#Transform Dictonary into a list with only the values
length_per_trait = list(count_of_traits_per_NFT.values())

# Input list initialization
Input = Trait_rarity_score

# list of length in which we have to split
length_to_split = length_per_trait

# Using islice
Inputt = iter(Input)
NFT_rarity_score = [sum(list(islice(Inputt, elem)))
          for elem in length_to_split]

# Printing Output
#print(Input)
#print("Split length list: ", length_to_split)

data = {'NFT_ID': NFT_ID,
        'NFT_Rarity_Score': NFT_rarity_score
        }

df = pd.DataFrame.from_dict(data).sort_values(by='NFT_Rarity_Score', ascending=False)

# Creating a new column with a rank
df['NFT_Ranking_Position'] = df['NFT_Rarity_Score'].rank(ascending=False)
Ranked_table = df.set_index('NFT_Ranking_Position')

#Return a table with the result
Ranked_table.head()
