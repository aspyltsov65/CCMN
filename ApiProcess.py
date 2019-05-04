import requests
import urllib3
import calendar_code
from requests.packages.urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings()


username = 'RO'
password_1 = 'just4reading'
password_2 = 'Passw0rd'

hostname = 'https://cisco-cmx.unit.ua/'
presence_host = "http://cisco-presence.unit.ua/"

query_mac = 'api/location/v1/history/clients/'
query_active = 'api/location/v2/clients/'
query_all_history = 'api/location/v1/history/clients'


def login():
    """Login to cisco-cmx.unit.ua, create request, get data from API"""
    session = requests.Session()
    session.auth = (username, password_1)
    session.verify = False
    response = session.get(hostname + query_active)
    return response.json()


def get_presence(from_date, to_date):
    """Create are GET request for get data about student presence"""
    session = requests.Session()
    session.auth = (username, password_2)
    session.verify = False
    response = session.get(presence_host + "api/presence/v1/dwell/count?siteId=1513804707441&startDate=" +
                           from_date + "&endDate=" + to_date)
    return response.json()
