import requests
import logging
from requests.structures import CaseInsensitiveDict
import json
from loadVars import load_settings


settings = load_settings()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def trackPackage(payload):

    # get api URL
    url = settings['url_17TrackGetTrackingDetails']
    logging.info(url)

    # setup header object for calling the API
    headers = setAPIHeaders(url)

    #verify payload before sending request
    #print("Request Payload:", json.dumps(payload, indent=4))

    # Send POST request for tracking info
    response = requests.post(url, headers=headers, data=payload)

    # Check if the request for tracking info was successful
    if response.status_code == 200:
        #print("Tracking info fetched successfully:")
        logging.info("Tracking info fetched successfully:")
        #print(json.dumps(response.json(), indent=4))
        #logging.info(response.json())
    else:
        #print("Failed to fetch tracking info. Error details:")
        logging.info("Failed to fetch tracking info. Error details:")
        #print(json.dumps(response.json(), indent=4))
        logging.error(json.dumps(response.json()))
    return response.json()

def registerPackage(payload):
    
    # get api URL
    url = settings['url_17TrackRegisterTrackingID']

    # setup header object for calling the API
    headers = setAPIHeaders(url)



    #verify payload before sending request
    #print("Request Payload:", json.dumps(payload, indent=4))
    

    # Send POST request for tracking info
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request for tracking info was successful
    if response.status_code == 200:
        logging.info("Tracking info fetched successfully:")
        #print(json.dumps(response.json(), indent=4))
    else:
        logging.info("Failed to fetch tracking info. Error details:")
        logging.info(json.dumps(response.json(), indent=4))
    return response.json()

def setAPIHeaders(url):
     # 17track API URLs
    api_Key = settings['api_key']
    
    # Headers
    headers = CaseInsensitiveDict()
    headers["17token"] = api_Key
    headers["Content-Type"] = "application/json"


    # Print the request details for debugging
    #print("Request URL:", url)
    #print("Request Headers:", headers)
    #print("Request Payload:", json.dumps(payload, indent=4))

    return headers