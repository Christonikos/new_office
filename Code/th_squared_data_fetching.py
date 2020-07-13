# =============================================================================
# MODULES, ALLIASES & GLOBALS
import requests, json
import pandas as pd
import numpy as np
import seaborn as sns
import os
from tqdm import tqdm  
from googletrans import Translator
api_key = 'AIzaSyDnMurqRmrbPdxCmDwmdhrkVHJhqNfj0i8'
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
join=os.path.join
make=os.makedirs
exists=os.path.exists
# =============================================================================


# =============================================================================
# DATA FETCHING & PREPROCESSING
# =============================================================================
def construct_search_query(key='accountant',town='Xanthi'):
    '''
    Create a search query based on the venue of interest and the town. 
    Translate the query in Greek to fetch venues with only Greek domains.
    
    Parameters
    ----------
    key: STR, 
        Provide the search target, optional.
        The default is 'accountant'.

    town: STR, optional
        Provide the name of the town that you'd wish to perform the search.
        The default is 'Xanthi'.

    Returns
    -------
    query: LIST.
        A list of all possible queries in English and Greek using the 
        provided parameters. The list includes capitalized and upper versions
        of the queries in both languages.

    '''
    translator = Translator()

    # To extend the search space create queries with and without determiners
    english_queries=[]
    for comb in range(0,6): #comb=combinations
        if comb==0:
            # simply combine with space
            tmp_query=(key+' '+town).strip()
        elif comb==1:
            # add a preposition
            tmp_query=(key+' in '+town).strip()
        elif comb==2:
            # capitalize each word
            tmp_query=(key.capitalize()+' '+town.capitalize()).strip()
        elif comb==3:
            # capitalize each word
            tmp_query=(key.capitalize()+' in '+town.capitalize()).strip()
        elif comb==4:
            # make upper
            tmp_query=(key.upper()+' in '+town.upper()).strip()   
        elif comb==5:
            # make upper
            tmp_query=(key.upper()+' '+town.upper()).strip()   
        english_queries.append(tmp_query)
    

    # Now translate the English queries to Greek and construct the search list
        
    translations = translator.translate(english_queries, dest='greek')
    greek_queries=[translations[i].text for i in range(0,len(translations))]
    # combine the queries from both languages
    queries=english_queries + greek_queries

    return queries

def fetch_data(queries,key='accountant',town='Xanthi'):
    '''
    Using the queries created with f'construct_search_query', 
    return the features of interest using the Google Places API.    

    Parameters
    ----------
    queries : LIST
        Queries and variants in English and Greek.

    Returns
    -------
    feature_matrix: DATAFRAME
    Contains the name, rating and coordinates of the place

    '''

    # features of interest (foi)
    foi=['name', 'user_ratings_total','rating', 'latitude', 'longitude']
    # Initialize containers for features of interest
    names, user_ratings_total,rating, rating, latitude, longitude=\
        ([] for i in range(0,6))
    
    for query in tqdm(queries):    
        # return response object 
        r = requests.get(url + 'query=' + query +
						'&key=' + api_key) 
        x = r.json()
        
        for result in range(0,len(x['results'])):
            names.append(x['results'][result]['name'])
            try:
                user_ratings_total.append(x['results'][result]['user_ratings_total'])
            except:
                print(f'{key, user_ratings_total} not found, setting to NaN')
                user_ratings_total.append(np.nan)
            try:    
                rating.append(x['results'][result]['rating'])
            except:
                print(f'{key, rating} not found, setting to NaN')
                rating.append(np.nan)
            latitude.append(x['results'][result]['geometry']['location']['lat'])
            longitude.append(x['results'][result]['geometry']['location']['lng'])
            

    # Construct dataframe
    df=pd.DataFrame(columns=foi)    
    df.name=names
    df.user_ratings_total=user_ratings_total
    df.rating=rating
    df.latitude=latitude
    df.longitude=longitude

    # Now remove duplicates
    df = df.drop_duplicates(subset='name', keep="first")
    # Save the dataframe locally
    path2data=join(os.path.realpath('..'),'Data', town)
    if not exists(path2data): make(path2data)
    fname=join(path2data,key+'_'+town+'.csv')
    df.to_csv(fname, encoding='utf-8-sig')
    
    return df


####################################################################
#   Fetch data for accountants, lawyers, and banks
####################################################################
keys=['accountant', 'lawyer','bank', 'insurer']
for town in ['Xanthi','Thessaloniki', 'Athens','heraklion', 'Patras']:
    for key in keys:
        print(key)
        # Get queries in English and Greek
        queries=construct_search_query(key,town)
        # Store preprocessed dataframes
        fetch_data(queries,key,town)


    