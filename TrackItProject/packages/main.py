
import json
import logging
from googlee import getSheetData, updateSheetData, getSheetCarriers
from loadVars import load_mystring
from OneSevenTrack import trackPackage, registerPackage
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main():
    #get all TrackingIDs from excel to track
    logging.info("Reading Excel file for tracking items")
    payload = getSheetData()
    logging.info("List of TrackingID's from Excel")
    logging.info(json.dumps(payload))
    
    #check for count of Tracking ID's as max allowed per call is 40
    if payload:
        # Splitting into chunks of 40
        chunks = [payload[i:i+40] for i in range(0, len(payload), 40)]
    
        for chunk in chunks:
            print(chunk)
            logging.info("Total Tracking ID Count > 40. Handling for 40+ ID's")
            logging.info("Sending request to 17Track API")
            data = trackPackage(json.dumps(chunk))
            #data = load_mystring()
            # Check if there are accepted rows
            if 'accepted' in data['data']:
                handleaccepted(data)        
            else:
                #print("No accepted rows found.")
                logging.info("No accepted rows found.")
            if 'rejected' in data['data']:
                handlerejectedforregistrationfailure(data['data']['rejected'])
            else:
                #print("No rejected rows found.")
                logging.info("No rejected rows found.")
            if 'errors' in data['data']:
                logging.error("Tracking API responded with errors")
                #print("retruned with error records")
                logging.info(data['data']['errors'])
    
    


def handlerejectedforregistrationfailure(rejected_rows):
        # Check if there are rejected rows due to missing registration
    logging.info("handling rejected tracking id's due to not registered")
    rejected_data = []
    if rejected_rows:
        for rejected_item in rejected_rows:
            if rejected_item["error"]["code"] == -18019902:
                rejected_data.append((rejected_item["number"]  ))
            if rejected_item["error"]["code"] == -18019909:
                handlerejectederror18019909(rejected_item)


        if rejected_data:
            registerPayload = getSheetCarriers(rejected_data)
            logging.info("Tracking ID's to be registered to track data")
            logging.info(registerPayload)
            response = registerPackage(registerPayload)
            logging.info("respons from registering ID's")
            logging.info(response)
            if response:
                acceptedreponse = response['data']['accepted']
                if acceptedreponse:                    
                    data = trackPackage(json.dumps(registerPayload))
                    handleaccepted(data)                    
                else: 
                    #print("Failed to register.")
                    logging.info("Failed to register")
            else: 
                #print("Failed to register.")
                logging.info("Failed to register")
        else: 
            #print("Failed to register.")
            logging.info("Failed to register")


def handlerejectederror18019909(data):
    logging.info("Handling rejected records as no tracking info available")
    tracking_data = []
    if data:
        for item in data:
            if 'number' in item:
                number = item['number']
            else: number = ""
            if 'error' in item:
                if 'code' in item: 
                    if 'message' in item:
                        latest_status = item['error']['code'] + item['error']['message']
                    else: latest_status = ""
                else: latest_status = ""
            else: 
                latest_status = ""            
                carrier = ""
                date = ""
                time = ""
                timezone = ""
                description = ""
                location = ""
                stage = ""
                latest_substatus = ""
                estimated_delivery = ""
                inforeceived_date = ""
            tracking_data.append((number, carrier, latest_status, date, time, timezone,  description, location, stage, latest_substatus,estimated_delivery,inforeceived_date))
        
    
    else:
        #print("No accepted rows found.")
        logging.info("No accepted rows found")
    
    logging.info("Updated Data to sheet")
    logging.info(tracking_data)
    updateSheetData(tracking_data)


def handleaccepted(data):
    logging.info("Handling accepted Tracking ID's")
    tracking_data = []
    accepted_rows = data['data']['accepted']
    if accepted_rows:
        for accepted_item in accepted_rows:
            number = ""
            carrier = ""
            latest_status = ""
            date = ""
            time = ""
            timezone = ""
            description = ""
            location = ""
            stage = ""
            latest_substatus = ""
            estimated_delivery = ""
            inforeceived_date = ""
            if 'number' in accepted_item:
                if accepted_item['number'] is not None:
                    number = accepted_item['number']
            if 'carrier' in accepted_item:
                if accepted_item['carrier'] is not None:
                    carrier = accepted_item['carrier']
            if 'track_info' in accepted_item:
                if 'latest_status' in accepted_item['track_info']:
                    if 'status' in accepted_item['track_info']['latest_status']:
                        if accepted_item['track_info']['latest_status']['status'] is not None:
                            latest_status = accepted_item['track_info']['latest_status']['status']
                if 'latest_event' in accepted_item['track_info']:
                    if 'time_raw' in accepted_item['track_info']['latest_event']: 
                        if 'date' in accepted_item['track_info']['latest_event']['time_raw']:
                            if accepted_item['track_info']['latest_event']['time_raw']['date'] is not None:
                                date = accepted_item['track_info']['latest_event']['time_raw']['date']
                        if 'time' in accepted_item['track_info']['latest_event']['time_raw']:
                            if accepted_item['track_info']['latest_event']['time_raw']['time'] is not None:
                                time = accepted_item['track_info']['latest_event']['time_raw']['time']
                        if 'timezone' in accepted_item['track_info']['latest_event']['time_raw']:
                            if accepted_item['track_info']['latest_event']['time_raw']['timezone'] is not None:
                                timezone = accepted_item['track_info']['latest_event']['time_raw']['timezone']
                    if 'description' in accepted_item['track_info']['latest_event']:
                        if accepted_item['track_info']['latest_event']['description'] is not None:
                            description = accepted_item['track_info']['latest_event']['description']
                    if 'location' in accepted_item['track_info']['latest_event']:
                        if accepted_item['track_info']['latest_event']['location'] is not None:
                            location = accepted_item['track_info']['latest_event']['location']
                    if 'stage' in accepted_item['track_info']['latest_event']:
                        if accepted_item['track_info']['latest_event']['stage'] is not None:
                            stage = accepted_item['track_info']['latest_event']['stage']
                    if 'sub_status' in accepted_item['track_info']['latest_event']:
                        if accepted_item['track_info']['latest_event']['sub_status'] is not None:
                            latest_substatus = accepted_item['track_info']['latest_event']['sub_status']                    
                """if 'time_metrics' in accepted_item['track_info']:
                    if 'estimated_delivery_date' in accepted_item['track_info']['time_metrics']:
                        if 'to' in accepted_item['track_info']['time_metrics']['estimated_delivery_date']:
                            if accepted_item['track_info']['time_metrics']['estimated_delivery_date']['to'] is not None:
                                estimated_delivery = accepted_item['track_info']['time_metrics']['estimated_delivery_date']['to']"""
                if 'tracking' in   accepted_item['track_info']:
                    if accepted_item['track_info']['tracking'] is not None:
                        if accepted_item['track_info']['tracking']['providers'] is not None:
                            for provider in accepted_item['track_info']['tracking']['providers']:
                                if provider['events'] is not None:
                                    for event in provider['events']:
                                        if event is not None:
                                            if event['sub_status'] is not None:
                                                if event['sub_status'] == 'Delivered_Other':
                                                    if event['time_raw'] is not None:
                                                        if event['time_raw']['date'] is not None:
                                                            estimated_delivery = event['time_raw']['date']
                if 'milestone' in  accepted_item['track_info']:
                    inforeceived_date = ""
                    if accepted_item['track_info']['milestone'] is not None:
                        milestones = accepted_item['track_info']['milestone']
                        if milestones:
                            for keystage in milestones:
                                if 'key_stage' in keystage:
                                    if keystage['key_stage'] is not None: 
                                        inforeceived = keystage['key_stage']
                                        if inforeceived == "InfoReceived":
                                            if keystage['time_raw']['date'] is not None:
                                                inforeceived_date = keystage['time_raw']['date']
                
            
               
            tracking_data.append((number, carrier, latest_status, date, time, timezone,  description, location, stage, latest_substatus,estimated_delivery,inforeceived_date))
        
    
    else:
        #print("No accepted rows found.")
        logging.info("No accepted rows found")
    
    logging.info("Updated Data to sheet")
    logging.info(tracking_data)
    updateSheetData(tracking_data)
    
   
    



if __name__ == '__main__':
    
    try:
        logging.info("************************New Run*************************")
        main()
    except Exception as e:
        # Handle the exception here
        # 'e' will contain information about the exception that was raised
        #print(f"An error occurred: {e}")
        logging.error("Unhandled exception")
        logging.critical(e)


