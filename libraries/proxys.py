import sys, random, json
import traceback
from re import findall, sub
from bs4 import BeautifulSoup
import requests
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

from requests.exceptions import ConnectionError

SSL = 'https://www.sslproxies.org/'
GOOGLE_ = 'https://www.google-proxy.net/'
ANANY = 'https://free-proxy-list.net/anonymous-proxy.html'
UK = 'https://free-proxy-list.net/uk-proxy.html'
US = 'https://www.us-proxy.org/'
NEW = 'https://free-proxy-list.net/'
SPYS_ME = 'http://spys.me/proxy.txt'
PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all'
PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
ALL = 'ALL'

def GOOGLE():
        proxy_https = []
        data = requests.get(GOOGLE_).text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table')

        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                ip = columns[0].text.strip()
                port = columns[1].text.strip()
                speed = columns[4].text.strip()

                insert = [ip, port, speed.replace("ms", "").strip()]
                proxy_https.append(insert)


        myarr = np.array(proxy_https)
        lists = myarr.tolist()

        data = [{
              'ip': item[0],
              'port': item[1],
              'type': item[2]
           }
           for i, item in enumerate(lists)
        ]

        json_data = json.dumps(data)
        proxy_https =  json.loads(json_data)
        return proxy_https

def HTTPS():
        proxy_https = []
        data = requests.get(PROXYLIST_DOWNLOAD_HTTPS).text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table')

        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                ip = columns[0].text.strip()
                port = columns[1].text.strip()
                speed = columns[4].text.strip()

                insert = [ip, port, speed.replace("ms", "").strip()]
                proxy_https.append(insert)


        myarr = np.array(proxy_https)
        lists = myarr.tolist()

        data = [{
              'ip': item[0],
              'port': item[1],
              'type': item[2]
           }
           for i, item in enumerate(lists)
        ]

        json_data = json.dumps(data)
        proxy_https =  json.loads(json_data)
        return proxy_https

def HTTP():
        proxy_http = [
        ["120.237.144.77",  9091,    "Elite" ,       361],
        ["103.127.1.130",   80,      "Transparent",  252],
        ["5.16.1.7",        1256,    "Transparent",  352],
        ["190.107.233.227", 999,     "Transparent",  261],
        ["112.49.34.128",   9091,    "Elite",        290],
        ["20.24.22.208",    8000,    "Elite",        140],
        ["23.94.98.201",    8080,    "Elite",        211],
        ["103.197.251.202", 80,      "Transparent",  321],
        ["169.57.1.85",     8123,    "Elite",        350],
        ["182.253.159.103", 8080,    "Transparent",  260],
        ["190.2.210.124",   999,     "Transparent",  121],
        ["117.54.114.96",   80,      "Anonymous",    241],
        ["154.83.29.206",   999,     "Elite",        110],
        ["218.28.98.229",   9091,    "Elite",        233],
        ["47.74.226.8",     5001,    "Elite",        342],
        ["212.23.217.67",   8080,    "Transparent",  254],
        ["91.189.177.190",  3128,    "Transparent",  110],
        ["43.255.113.232",  81,      "Elite",        153],
        ["111.85.159.65",   9091,    "Elite",        189],
        ["139.9.64.238",    443,     "Anonymous",    284],
        ["20.24.22.143",    8000,    "Elite",        228],
        ["95.217.62.36",    3128,    "Transparent",  308],
        ["54.36.26.122",    80,      "Elite",       181],
        ["182.253.109.182", 8080,    "Transparent",  392],
        ["193.122.71.184",  3128,    "Transparent",  93],
        ["20.111.54.16",    8123,    "Elite",        215],
        ["0.111.54.16",     80,       "Elite",       329],
        ["45.169.162.1",    3128,     "Elite",       262],
        ["130.41.55.190",   8080,    "Anonymous",    136],
        ["66.94.113.79",    3128,    "Transparent",  105],
        ["177.12.238.100",  3128,    "Elite",        127],
        ["103.115.26.254",  80,      "Transparent",  141],
        ["20.111.47.44",    8000,    "Elite",        363],
        ["117.54.114.103",  80,      "Anonymous",    368],
        ["115.243.238.43",  80,      "Anonymous" ,   95],
        ["46.101.126.180",  34969,   "Elite",        139],
        ["117.160.132.37",  9091,    "Elite",        342],
        ["62.193.108.144",  1976,    "Transparent",  199],
        ["8.219.97.248",    80,      "Elite",        120],
        ["20.206.106.192",  8123,    "Elite",        347],
        ["43.230.123.14",   80,      "Transparent",  178],
        ["223.112.174.62",  9091,    "Elite",       310],
        ["190.2.215.210",   999,     "Transparent",  130],
        ["103.149.162.195", 80,      "Elite",        179],
        ["20.230.193.232",  80,      "Elite",        156],
        ["112.53.167.29",   9091,    "Elite",        140],
        ["39.164.100.105",  9091,    "Elite" ,       274],
        ["170.254.201.40",  3180,    "Transparent",  375],
        ["165.154.225.65",  80,      "Elite",        150],
        ["183.239.61.167",  9091,    "Elite",        355],
        ["42.228.61.245",   9091,    "Elite",        281],
        ["120.237.144.77",  9091,    "Elite",        361],
        ["139.99.237.62",   80,      "Elite",        175],
        ["143.244.45.5",    3128,    "Transparent",  266],
        ["208.52.145.196",  5555,    "Transpar",    116],
        ["208.52.180.53",   5555,    "Transparent",  228],
        ["195.135.243.41",  8080,    "Transparent",  210],
        ["45.142.106.202",  80,      "Elite",        253],
        ["111.59.117.17",   9091,    "Elite",        148],
        ["118.212.152.82",  9091,    "Elite",       220],
        ["154.7.6.96",      80,      "Transparent",   262],
        ["20.24.43.214",    8123,    "Elite",         149],
        ["125.42.2.148",    9091,    "Elite",         223],
        ["1.10.157.128",    80,      "Anonymous",     299],
        ["117.54.114.98",   80,      "Anonymous",     316],
        ["192.99.92.27",    5555,    "Elite",         167],
        ["165.154.226.242", 80,      "Elite",         129],
        ["80.48.119.28",    8080,    "Elite",         248],
        ["154.83.29.200",   999,     "Elite",         346],
        ["208.52.166.111",  5555,    "Transparent",   95],
        ["51.38.191.151",   80,      "Elite",         217],
        ["123.163.48.229",  9091,    "Elite",         137],
        ["41.33.63.182",    1981,    "Transparent",   222],
        ["154.236.189.26",  1976,    "Transparent",   268],
        ["62.193.68.85",    1976,    "Transparent",   185],
        ["41.65.227.163",   1981,    "Transparent",   270],
        ["101.32.35.72",    80,      "Transparent",   394],
        ["203.89.126.250",  80,      "Transparent",   252],
        ["211.138.6.37",    9091,    "Elite",         274],
        ["218.75.38.154",   9091,    "Elite",         344],
        ["208.52.145.214",  5555,    "Transparent",   283],
        ["190.26.201.194",  8080,    "Transparent",   145],
        ["208.52.145.225",  5555,    "Transparent",   233],
        ["168.90.255.60",   999,     "Transparent",   120],
        ["130.41.15.76",    8080,    "Anonymous",     299],
        ["45.177.108.4",    999,     "Transparent",   248],
        ["91.189.177.186",  3128,    "Transparent",   295],
        ["173.68.63.231",   8080,    "Elite",         195],
        ["103.117.192.14",  80,      "Transparent",   377],
        ["124.131.219.94",  9091,    "Elite",         300],
        ["183.111.25.250",  8080,    "Transparent",   290],
        ["91.189.177.189",  3128,    "Transparent",   106],
        ["58.17.24.162",    9091,    "Elite",         207],
        ["61.182.121.66",   9091,    "Elite",         397],
        ["112.4.232.168",   9091,    "Elite",         231],
        ["129.152.19.129",  3128,    "Transparent",   150],
        ["112.36.17.39",    9091,    "Elite",         227],
        ["183.88.179.50",   8088,    "Transparent",   93],
        ["103.154.65.122",  8080,    "Transparent",   293],
        ["91.144.158.238",  8080,    "Transparent",   157],
        ["154.83.29.201",   999,     "Elite",         192],
        ["111.160.204.146", 9091,    "Elite",         345],
        ["139.99.237.62",   80,      "Elite",         175],
        ["20.111.54.16",    8123,    "Elite",         215],
        ["54.36.226.226",   2019,    "Transparent",   363],
        ["103.206.51.225",  84,      "Transparent",   294],
        ["103.117.192.174", 80,      "Transparent",   177],
        ["43.132.148.107",  2080,    "Transparent",   255],
        ]

        data = requests.get(PROXYLIST_DOWNLOAD_HTTP).text
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table')

        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            
            if(columns != []):
                ip = columns[0].text.strip()
                port = columns[1].text.strip()
                speed = columns[4].text.strip()

                insert = [ip, port, speed.replace("ms", "").strip()]
                proxy_http.append(insert)


        myarr = np.array(proxy_http)
        lists = myarr.tolist()

        data = [{
              'ip': item[0],
              'port': item[1],
              'type': item[2]
           }
           for i, item in enumerate(lists)
        ]

        json_data = json.dumps(data)
        proxy_http =  json.loads(json_data)
        return proxy_http

google_proxy = GOOGLE
https_proxy = HTTPS
http_proxy = HTTP