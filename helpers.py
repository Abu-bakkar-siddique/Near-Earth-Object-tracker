import csv
from datetime import datetime, timedelta
import re
import pytz
import requests
import subprocess
import urllib

from flask import redirect, render_template, session
from functools import wraps

def validate_email(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    result = re.fullmatch(regex, email)
    if result:
        return True
    return False

def extract_neo_info(neo):
    return {
        "name": neo['name'],
        "estimated_diameter_kms": neo['estimated_diameter']['kilometers']['estimated_diameter_min'],
        "close_approach_date_full": neo['close_approach_data'][0]['close_approach_date_full'],
        "relative_velocity_kps": neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
        "miss_distance_kilometer": neo['close_approach_data'][0]['miss_distance']['kilometers']
    }

def get_neo(start_date, end_date):
    base_url = "https://api.nasa.gov/neo/rest/v1/feed"
    my_key = "bz49Hv4NdWEZ5DrV0NyWuCtL2ZZLMWNT7L3Nj8Ea"

    # Construct the API URL with the specified parameters
    url = f"{base_url}?start_date={start_date}&end_date={end_date}&api_key={my_key}"
    data = requests.get(url).json()
    # Assuming 'data' contains the entire JSON response
    neos_info = []

    # Extract information for the first 20 NEOs
    count = 0
    for date, neos in data['near_earth_objects'].items():
        for neo in neos:
            neos_info.append(extract_neo_info(neo))
            count += 1
            if count == 20:
                break
        if count == 20:
            break

    # Return the result
    result = {"near_earth_objects": neos_info}
    #print(result['near_earth_objects'][1]["name"])
    for i in range(len(result['near_earth_objects'])):
        for val in result['near_earth_objects']:
            print(val)
    return result['near_earth_objects']


#get_neo("2021-04-24","2021-04-25")


def authenticate(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorated