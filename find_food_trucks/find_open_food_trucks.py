#import libraries
import requests
import pandas as pd
from datetime import datetime


def load_data(data_url):
    '''
    This function makes an API request to the url and retrieves the data from url.
    It converts json body content from the response to dataframe and returns it.
    '''
    try:
        #API request to retreive data from url (https://dev.socrata.com/foundry/data.sfgov.org/jjew-r69b
        response = requests.get(data_url)
        #when No error in retrieving data, extract the JSON body content from the response 
        data = response.json()
        response.raise_for_status()
    #catch an HTTPError under the variable name exception
    except requests.exceptions.HTTPError as exception:
        #print exception and exit
        print(exception)
        exit(0)  
    #convert json to dataframe
    return pd.json_normalize(data)
  

def get_current_datetime():
    '''
    This function returns the current local date and time
    '''
     #returns the current local date and time in the format YYYY-MM-DD HR:MIN:SEC
    return datetime.now()

def get_current_dayofweek(curr_datetime):
    '''
    This function returns the current day of Week
    '''
    #formats datetime into readable format strings(Weekday as a number)
    return curr_datetime.strftime("%w")

def get_current_time24(curr_datetime):
    '''
    This function returns the time in minutes
    '''
    #convert time to minutes
    return curr_datetime.hour*60+curr_datetime.minute+curr_datetime.second/60

def find_open_foodtrucks(day_week,time_24,data_find):
    '''
    This function takes the data and filters based on the weekday and time .
    Sort the results alphabetically by name and return the filtered dataframe
    '''

    # dataset has start24 and end24 in HH:MM format . Lets convert the time to minutes for comparison
    data_find["start24_min"]=data_find["start24"].apply(
        lambda x: int(x.split(':')[0])*60+int(x.split(':')[1])
        )
    data_find["end24_min"]=data_find["end24"].apply(
        lambda x: int(x.split(':')[0])*60+int(x.split(':')[1])
        )

    #we have two columns dayoforder(numeric) and dayofweekstr(str) in the dataset for weekday
    #Using dayoforder(numeric), filter dataframe based on the weekday
    data_filtered=data_find[data_find["dayorder"]==day_week]
    #compare if the current time in minutes is between start and end time and select only applicant 
    # and location columns
    data_filter_time=data_filtered[(
        data_filtered["start24_min"]<=time_24
        )&(
        data_filtered["end24_min"]>=time_24
        )][["applicant","location"]]
    #Rename columns and sort alphabetically by name
    data_transformed=data_filter_time.sort_values("applicant").rename(
        columns={"applicant":"NAME","location":"ADDRESS"} 
        ).reset_index(drop=True)
    #return transformed dataframe
    return data_transformed