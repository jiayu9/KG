import requests
import pandas as pd
import os
def key_to_entity(id):
    
    API_KEY = 'AIzaSyDIC3blvZHi3X17jzHsyHN1TctL135arLo'
    SEARCH_ENGINE_KEY = 'b2a6cd70a00c54897'
    search_query = id #/m/02pt6k_

    url = 'https://www.googleapis.com/customsearch/v1'
    
    params={
        'q': search_query,
        'key': API_KEY,
        'cx' : SEARCH_ENGINE_KEY
    }
    headers = {
    'Accept': 'application/json'
    }

    wiki_url=''
    
    response1=requests.get(url,params=params,headers=headers)
    results1=response1.json()
    
    try:
        if 'items' in results1:
            web_link=results1['items'][0]['link']
            wiki_url=web_link.replace('/wiki','/entity') #https://www.wikidata.org/wiki/Q6963000
            entity_id=wiki_url.split('/')[-1] #Q6963000

        if wiki_url=='':
            print(id+' url not found')
            return
        
    except:
        print(id+' url not found')
        return

    
    
    try:
        response2=requests.get(wiki_url,params=params)
        results2=response2.json()
        entity_name=results2['entities'][entity_id]['labels']['en']['value'] #Nancy Snyderman
    except:
        print(id+' entity not found')
        return



    if os.path.exists('key_to_entity.csv'):
        write_mode = 'a'  # append mode
        header = False    # do not write the header again
    else:
        write_mode = 'w'  # write mode (create file)
        header = True     # write the header
    # Create a dictionary with the data
    data = {
        'fb_id': [id],
        'url': [wiki_url],
        'entity_name': [entity_name]
    }

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv('key_to_entity.csv',mode=write_mode, header=header)    

# key_to_entity('/m.0695j')
# key_to_entity('/m/02pt6k_')
key_to_entity('/m/03115z')