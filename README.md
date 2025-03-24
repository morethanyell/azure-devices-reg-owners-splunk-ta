# Splunk Technology Add-on for Microsoft Graph Devices Registered Owners
## Overview
The Splunk-built TA for Azure endpoints (TA-MS-AAD) has input stanza for Devices but it doesn't allow for the `registeredOwners` to be included. Here's a [reference](https://learn.microsoft.com/en-us/graph/api/device-list-registeredowners) for this MS Graph endpoint.

## Features
✅ Expands `registeredOwners` to retrieve user details \
✅ Allows for optional Query Parameters \
✅ Excludes empty registeredOwners for cleaner data \
✅ Handles pagination to retrieve all results \
✅ Purposely excluded all the other fields from `devices` endpoint because it's already supplied by TA-MS-AAD, get it [here](https://splunkbase.splunk.com/app/3757)

## Requirements

- An Azure app-registration (that's your Client ID) 
- This Client ID muyst have `Device.Read.All`

## How to make it work
- Install this on your HF or SplunkCloud stack
- Create an input stanza
- Give it a name
- Give it a very long interval (you don't need this that much, once per day is fine: 86400)
- Enter your Client ID, Client Secret, and the Azure Directory Tenant ID
- Enter the index you wish to dump these events (they're not events, btw. just a dump of user accounts with specific information)
- Optionally enter MS Graph OData Query Parametrs, e.g.: `$filter(operatingSystem eq 'Windows')`

## Sample log

```
   displayName: BILLGATES-MACBOOK
   id: caa7f06d-1359-4df3-8f9e-a5fdbd994c2e
   registeredOwners: [ [-]
     { [-]
       @odata.type: #microsoft.graph.user
       id: 45d550b6-7225-4110-a942-91a353f2cdea
       userPrincipalName: william.gates@usesmacbooks.com
     }
   ]
```

## Beers accepted
daniel.l.astillero@gmail.com