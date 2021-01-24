#!/usr/bin/env python3
#import libraries
from tabulate import tabulate
import colorama
from colorama import Fore, Back, Style
from find_food_trucks import find_open_food_trucks 
import time

url = "http://data.sfgov.org/resource/bbb8-hzi6.json"

def waitbeforexit():
    '''
    This functions waits for 1 sec before it exits the program or loop
    '''
    time.sleep(1)
    print(Style.BRIGHT+Fore.RED+Back.WHITE+"trying to exit...."+reset_style)
    exit(0)

def display_food_trucks_open(data_display):
    '''
    This function displays food trucks that are open 
    '''
    #clear screen
    clear_screen='\033c'
    #if no food trucks that are open 
    if datafiltered.empty :
        print(clear_screen)
        print("------------------------------------------------------------------------------------------------")
        print(Style.BRIGHT+Fore.CYAN + "No Food Tucks open at this time" +reset_style)
        print("------------------------------------------------------------------------------------------------")
        waitbeforexit()
    #print the number of food trucks open
    else:
        print(Style.BRIGHT)
        print(clear_screen+Fore.CYAN +"Found",len(datafiltered),"food trucks that are open"+reset_style)
       
    #iterate the dataframe and display the food trucks open and wait for input from the user
    list_iterate=list(range(0,len(datafiltered),10))  
    for pagenum,index in enumerate(list_iterate):
        print("------------------------------------------------------------------------------------------------")
        datafiltered_noindex=datafiltered.iloc[index:index+10]
        # use tabulate to add tables to the dataframe 
        print(tabulate(datafiltered_noindex,headers=datafiltered.columns,tablefmt='github',showindex=False))
        print("------------------------------------------------------------------------------------------------")
        print(Fore.CYAN+"                          Page "+str(pagenum+1)+" of "+str(len(list_iterate))+reset_style)
        print("------------------------------------------------------------------------------------------------")  
        #print End of page when no more food trucks open to be displayed
        if pagenum==len(list_iterate)-1:
            print(Style.BRIGHT+Fore.GREEN+"End of Page"+reset_style)
            waitbeforexit()
        print(Fore.GREEN+"Press \"Enter\" to display more food trucks that are open at this time or Press \'Q\' to exit :"+reset_style,end='') 
        input_key_press=input()
        if (input_key_press == ""):
            continue
        elif (input_key_press.lower() == 'q'):
            waitbeforexit()
        else:
            print("-------------------------------------------------------------------------------------------------")     
            print(Style.BRIGHT+Fore.RED+Back.WHITE+'None of the specified options were chosen'+reset_style)
            print(Fore.GREEN+"Display more food trucks that are open (Y/N):"+reset_style,end='')
            key_press=input()
            if (key_press.lower() == "y"):
                continue
            elif(key_press.lower() == "n"):
                waitbeforexit()
            else:
                print(Style.BRIGHT+Fore.RED+Back.WHITE+'None of the specified options were chosen'+reset_style)
                waitbeforexit()
        

if __name__=="__main__":
    #coloroma Python library for coloring text in an easy way that works across all platforms 
    #initialize colorama
    colorama.init()
    #reset style set for coloring text
    reset_style='\033[0m'
    #load data
    data_normalized =find_open_food_trucks.load_data(url)
    #get current datetime
    date_time=find_open_food_trucks.get_current_datetime()
    #get current weekday 
    dayofweek=find_open_food_trucks.get_current_dayofweek(date_time)
    #get current time in minutes
    time24=find_open_food_trucks.get_current_time24(date_time)
    #find open food trucks at the current time
    datafiltered= find_open_food_trucks.find_open_foodtrucks(dayofweek,time24,data_normalized)
    #display the results 
    display_food_trucks_open(datafiltered)
