
# encoding = utf-8

import os
import sys
import time
import datetime
import requests
import json
import random

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''


def get_access_token(helper, client_id, client_secret, token_url):
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    
    helper.log_info("Retrieving access token from Graph.")
    
    try:
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_info = response.json()
        
        helper.log_info(f"Access token for client id {client_id} has been granted...")
        
        return token_info['access_token']
    except requests.RequestException as e:
        helper.log_error(f"Error obtaining token: {e}")
        return None

def get_registered_owners(helper, token, url):
    
    headers = {"Authorization": f"Bearer {token}"}
    all_devices = []
    
    # Let Splunk investigators know that collection is still alive
    if random.random() < 0.03:
        helper.log_info(f"Still querying Microsoft Graph for /devices/registeredOwners...")

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise error if request fails
    data = response.json()

    # Extract and filter fields while excluding empty registeredOwners and checking trustType
    filtered_devices = [
        {
            "id": device.get("id"),
            "displayName": device.get("displayName"),
            "registeredOwners": device.get("registeredOwners")
        }
        for device in data.get("value", []) 
        if device.get("registeredOwners")  # Ensure registeredOwners is not empty/null
    ]

    all_devices.extend(filtered_devices)

    # Check for pagination link (if more data exists)
    next_url = data.get("@odata.nextLink")

    return all_devices, next_url

def validate_input(helper, definition):
    pass

def collect_events(helper, ew):
    CLIENT_ID = helper.get_arg('app_client_id')
    CLIENT_SECRET = helper.get_arg('client_secret')
    TENANT_ID = helper.get_arg('tenant_id')
    QPARAM = helper.get_arg('query_parameters')
    
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    log_level = helper.get_log_level()
    
    helper.set_log_level(log_level)
    
    helper.log_info(f"Start of collection.")
    helper.log_info(f"Logging level is set to: {log_level}")
    helper.log_info(f"Collecting Azure Devices Registered Owners from Azure tenant {TENANT_ID}, using app/client {CLIENT_ID}")
    
    meta_source = f"ms_aad_device:tenant_id:{TENANT_ID}"
    
    try:

        token = get_access_token(helper, CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
        next_url = f"https://graph.microsoft.com/beta/devices?$expand=registeredOwners($select=id,userPrincipalName)&$select=id,displayName&{QPARAM}"
        
        helper.log_info(f"Now retrieving data from MS Graph Devices. OData Query Parameters: $expand='registeredOwners' $select='id,displayName' {QPARAM}".rstrip())
        
        while next_url:
            
            registered_owners, next_url = get_registered_owners(helper, token, next_url)
        
            for ro in registered_owners:
        
                data_event = json.dumps(ro, separators=(",", ":"))
                
                event = helper.new_event(source=meta_source, index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data_event)
            
            ew.write_event(event)
        
        helper.log_info("End of collection.")
        
    except Exception as e:
        helper.log_error(f"Error processing Azure Devices Registered Owners.: {e}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
