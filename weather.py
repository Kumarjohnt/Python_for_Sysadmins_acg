
#!"G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\venvs\experiment\Scripts\python.exe"


## script runs in venv/experiment only as requests module is installed in venv.

# & 'G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\venvs\experiment\Scripts\python.exe' "g:/My Drive/Scripts/Python/Python_for_Sysadmins_ACG/Python_for_Sysadmins_acg/weather.py" 560076

import os 
import requests
import sys

from argparse import ArgumentParser

parser = ArgumentParser(description='Get the current weather information for your zipcode')
parser.add_argument('zip', help='zip/postal code to get weather for')
parser.add_argument('--country',default='in', help='country zip/postal belons to, defaults to India')

args = parser.parse_args()


api_key = '84f89d4dc579508db4d302f3a604c28e'

if not api_key:
    print("Error: No API key provided")

url = f"https://api.openweathermap.org/data/2.5/weather?zip={args.zip},{args.country}&appid={api_key}"

# print(url)

res = requests.get(url)

print(res)

if res.status_code != 200:
    print(f"Error talking to weather provider: {res.status_code}")
    sys.exit(1)

print(res.json())
