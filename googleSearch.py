#!/usr/bin/env python3
#%%
import math
import pandas
from googlesearch import search

#%%
##############
# Settings
##############

verbose = True

#%%
##############
# User Input
##############

query = input("Enter Search Query: ")
print(f"Search Query is: {query}")

try:
    num_results= int(input("Enter number of results: "))
except ValueError:
    print('Please enter a whole number')
print(f"Number of results is: {num_results}")

filename = str(input("Enter filename to save results: "))
print(f"Filename to save results is: {filename}")

if str(input("Is this correct?' (y/n): ")).lower().strip() != 'y':
    print("Input not confirmed, quitting")
    exit()

#%%
##############
#Fetch Results
##############

print("Fetching Results from Google")
search_results = pandas.DataFrame(search(query,
                            num_results=num_results, verbose=verbose))
#%%
##############
#Save Results
##############

print(f"Savings results in file {filename}")
search_results.to_csv(filename, index=False)
