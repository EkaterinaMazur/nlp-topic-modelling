###################
### PREPARATION ###
###################

### IMPORT PACKAGES
# general packages
import os
import logging
import requests

### SETUP LOGGING
# to do

#########################
### REQUEST RESPONSES ###
#########################

### TWEEDE-KAMER
# set variables, use this later
tk_api_root = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/'
sub = 'Document'
sub = 'Reservering?$top=25'
params = {}
# requests response
response = requests.get(tk_api_root+sub)
# get json version
response = response.json()
# print length
print(f"""We've got a response with {response.json().keys()} as keys from {str(response.json()['@odata.context'])}, with the value key containing {len(response.json()['value'])} items""")


### OFFICIELE BEKENDMAKINGEN
# set variables
ob_api_root = 'https://zoek.officielebekendmakingen.nl/kst-'
dossier = 34324         # THIS DOSSIER DOES NOT EXIST, REPLACE WITH EXISTING DOSSIER IF YOU WANT IT TO WORK

# request response
response = requests.get(ob_api_root+str(dossier))