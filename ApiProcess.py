
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

siteId = str(presenceSession.get(presence_host + "api/config/v1/sites").json()[0]['aesUId'])
print(siteId)


def get_active():
    """Login to cisco-cmx.unit.ua, create request, get data from API"""
    response = localSession.get(local_host + query_active)
    return response.json()


def get_presence(from_date, to_date):
    """This API returns the count of visitors categorized by dwell level seen on a given day or date range"""
    response = presenceSession.get(presence_host + "api/presence/v1/dwell/count?siteId=" + siteId +
                                   "&startDate=" + from_date + "&endDate=" + to_date)
    return response.json()


def get_repeat_visitors(from_date, to_date):
    """This API returns the average count of repeat visitors seen for the specified date range"""

    response = presenceSession.get(presence_host + "api/presence/v1/repeatvisitors/average?siteId=" + siteId
                                   + "&startDate=" + from_date + "&endDate=" + to_date)
    return response.json()


def get_peak():
    """This API returns the hour that had peak visitors today"""

    return presenceSession.get(presence_host + 'api/presence/v1/visitor/today/peakhour?siteId=' + siteId).json()


def get_today_visitors():
    """This API returns the count of visitors seen today until now"""

    return presenceSession.get(presence_host + 'api/presence/v1/visitor/count/today?siteId=' + siteId).json()


def get_yesterday_visitors():
    """This API returns the count of repeat visitors seen yesterday"""

    return presenceSession.get(presence_host + 'api/presence/v1/visitor/count/yesterday?siteId=' + siteId).json()


def get_day_count_students():
    """This API returns the daily count of connected visitors for the last 7 days"""

    response = presenceSession.get(presence_host + 'api/presence/v1/connected/daily/lastweek?siteId=' + siteId)
    return response.json()


def get_total_connected():
    """This API returns the count of connected visitors seen today until now"""

    return presenceSession.get(presence_host + 'api/presence/v1/connected/count/today?siteId=' + siteId).json()


# Dwell time

def get_average_visitor_dwell_time_for_today():
    """This API returns the average visitor dwell time in minutes for today until now"""

    return presenceSession.get(presence_host + 'api/presence/v1/dwell/average/today?siteId=' + siteId).json()


def get_count_of_visitors_by_dwell_level_for_today():
    """This API returns the count of visitors categorized by dwell level seen today until now"""

    return presenceSession.get(presence_host + 'api/presence/v1/dwell/count/today?siteId=' + siteId).json()
