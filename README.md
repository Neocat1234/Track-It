# Track-It Project

## Project takes a set list of tracking id's on a google spreadsheet and auto-updates information about them (date, time, EST Arrival, etc.)

This project was built using various API's: Google's Sheets API, Google's Drive API, and 17track's API.
It is intended to take a set of tracking ID's that are in a specific cell, and return information automatically (every x amount of mins) about the ID.
Currently, the only carriers that will work with this code are Fedex, UPS, and USPS. 
The information returned will include: EST Arrival (time & date), Current Status (In transit, Delayed, etc.) and what date the status was updated, and Date Shipped. 


