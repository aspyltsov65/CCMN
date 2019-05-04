import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


username = 'RO'
password_1 = 'just4reading'
password_2 = 'Passw0rd'

local_host = 'https://cisco-cmx.unit.ua/'
presence_host = "http://cisco-presence.unit.ua/"

query_mac = 'api/location/v1/history/clients/'
query_active = 'api/location/v2/clients/'
query_all_history = 'api/location/v1/history/clients'

localSession = requests.Session()
localSession.auth = (username, password_1)
localSession.verify = False

presenceSession = requests.Session()
presenceSession.auth = (username, password_2)
presenceSession.verify = False

def get_active():
    """Login to cisco-cmx.unit.ua, create request, get data from API"""

    return localSession.get(local_host + query_active).json()


def get_presence(from_date, to_date):
    """Create are GET request for get data about student presence"""
    response = presenceSession.get(presence_host + "api/presence/v1/dwell/count?siteId=1513804707441&startDate=" +
                           from_date + "&endDate=" + to_date)
    return response.json()


def get_repeat_visitors(from_date, to_date):
    """ """
    response = presenceSession.get(presence_host +
                                   "api/presence/v1/repeatvisitors/average?siteId=1513804707441&startDate=" +
                                   from_date + "&endDate=" + to_date)
    return response.json()


def get_peak():
    """ """
    return presenceSession.get(presence_host + 'api/presence/v1/visitor/today/peakhour?siteId=1513804707441').json()


def get_today_visitors():
    """ """
    return presenceSession.get(presence_host + 'api/presence/v1/visitor/count/today?siteId=1513804707441').json()


def get_yesterday_visitors():
    """ """
    return presenceSession.get(presence_host + 'api/presence/v1/visitor/count/yesterday?siteId=1513804707441').json()
