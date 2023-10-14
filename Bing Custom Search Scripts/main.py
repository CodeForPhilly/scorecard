import pandas as pd
import numpy as np
from helpers import make_request

from dotenv import load_dotenv
import os

load_dotenv()
credentials = os.getenv("SUBSCRIPTION_KEY")


#Read in the data from the excel sheet - URLS and Search Strings
URLsToScrape = pd.read_excel("input.xlsx",sheet_name="INPUT_URLsToScrape")
TopicsToLookFor = pd.read_excel("input.xlsx",sheet_name="INPUT_TopicsToLookFor")


#Create a dictionary of the following structure - {"topic|subtopic":[list of substrings]}
search_string_dict = {}
for _, row in TopicsToLookFor.iterrows():

    key = row["Topic"] + "|" + row["Sub Topics"]
    
    search_string_dict[key] = [row[f"Search String {num}"] for num in [1,2,3,4] if row[f"Search String {num}"] is not np.nan]



#For each url for each topic for each search string GET "https://api.bing.microsoft.com/v7.0/custom/search" with q = "search string" + site:https://www.eastpikeland.org/
#Check if search string in name
#If it is, add it to a dataframe with the url,url_name and data from URLsToScrape

output_df = None

###Remove this after testing###
#townships_searchstring = [("East Pikeland","Native Plants"), ("Easttown","Rain Garden"),("East Pikeland","Environmental Advisory Council"),("Kennett","Dark Skies"),("Kennett","Rain Garden")]
###############################

for _,row in URLsToScrape.iterrows():

    for topic_subtopic, search_string_list in search_string_dict.items():

        for search_string in search_string_list:

            search_string = search_string.strip()

            ###Remove this after testing###
            #if (row["Township / Borough"],search_string) not in townships_searchstring:
                #continue
            ###############################

            json_response_dict = make_request(search_string,row["google prefix"],credentials)

            if "webPages" not in json_response_dict:
                continue

            #TODO:Should broaden this check by preprocessing the name to catch names like Native-Invasive-Plants, Native-Plants
            #Write some regex 
            #Should also check url (maybe)

            if search_string not in json_response_dict["webPages"]["value"][0]["name"]:
                continue

            else:
                print((row["Township / Borough"],search_string))
                
                new_row = pd.DataFrame({"Township or Borough":[row["Township or Borough"]],
                           "Township / Borough":[row["Township / Borough"]],
                           "County":[row["County"]],
                           "State":[row["State"]],
                           "Related Topic":[topic_subtopic.split("|")[0]],
                           "Sub Topic":[topic_subtopic.split("|")[1]],
                           "URL Title": [json_response_dict["webPages"]["value"][0]["name"]],
                           "URL":[json_response_dict["webPages"]["value"][0]["url"]]})
                
                if output_df is None:
                    output_df = new_row
                else:
                    output_df = pd.concat([output_df,new_row],ignore_index=True)

output_df.to_csv("output.csv")





