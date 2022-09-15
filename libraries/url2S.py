from googleapiclient.discovery import build
from pysafebrowsing import SafeBrowsing
from urllib.parse import urlparse
import requests, json, random
from duckduckgo_search.utils import session
from duckduckgo_search import ddg as engine
import random


try:
	from libraries.errorhandler import FailedApi, HttpsError
	from libraries.api import Api_Validate, User_Agent
except:
	try:
		from errorhandler import FailedApi, HttpsError
		from api import Api_Validate, User_Agent
	except:
		from Tera_Search.libraries.errorhandler import FailedApi, HttpsError
		from Tera_Search.libraries.api import Api_Validate, User_Agent

sesions = []
if not sesions:	
	Api_Validate("hello", requests.Session())
	sesions.append(1)

class safebrowsing:
	"""docstring for safebrowsing"""
	def __init__(self, api_key):
		super(safebrowsing, self).__init__()
		self.reqs = SafeBrowsing(api_key)

	def run(self, urls):
		output = self.reqs.lookup_urls([urls])
		keys = list(output.keys())[0]
		point = 0
		if output[keys]['malicious'] == False:
			point +=1
		if urlparse(urls).scheme=="https":
			point +=1
		return self.checkpoint(point)

	def checkpoint(self, point):
		pass
		if point == 2:
			return "safe"
		elif point == 1:
			return "warning"
		else:
			return "danger"


class SearchGoogle:
	"""docstring for SearchGoogle"""
	def __init__(self, api_key):
		super(SearchGoogle, self).__init__()
		self.reqs = build('customsearch', 'v1', developerKey=api_key).cse()
		self.client = "e13e6bab6d2274321"

	def search_default(self, searchs):
		output = []
		for i in range(1, 6, 10):
			result =self.reqs.list(q=searchs, cx=self.client, start=i).execute()
			output+= result['items']
		return output








#///////////////////////////Duck-Duck




class Duck2Engine:
	
	"""docstring for Duck2Engine"""

	def __init__(self):
		super(Duck2Engine, self).__init__()
		self.regmethod = ''
		self.results = ''
   
	def searchs(self, searchs, user_agent='default', region=None,time=None, max_results=600, proxy=None):
		if max_results<=900:
			max_results = max_results
		else:
			max_results = 600

		if proxy:
			proxys = proxy
		else:
			proxys = {}
		if region:
			region = 'wt-wt'
		else:
			region = self.regmethod

		if user_agent == "default" or user_agent is "default":
			pass
		else:
			set_agent = User_Agent(random)
			if user_agent == "bot":
				agents = set_agent.bot()
			else:
				agents = set_agent.get()
			headers = {
				    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
				    "Referer": "https://duckduckgo.com/",
				    }
			session.headers.update(headers)
			session.proxies = proxys


		try:
			results = engine(searchs, region=region, time=time, max_results=max_results)
		except:
			results = engine(searchs, region=region, time=None, max_results=max_results)
		random.shuffle(results)
		self.results = results

	def result(self):
		results = self.results
		class result:
			def __init__(self):
				super(result, self).__init__()
			def json(self):
				datas = {}
				datas.update({'result':results})
				return datas
			def list(self):
				return results
		return result()

	def region(self, reg):
		switcher = {'wt': 'wt-wt', 'us': 'us-en', 'uk': 'uk-en', 'ru': 'ru-ru', 'etc': 'etc'}
		def search_mount(month):
					for x in switcher:
						if any(reg.lower() in s for s in x.split(" "))==True:
							return x
						else:
							if any(x.lower() in s for s in reg.lower().split(" "))==True:
								return x
					return 'us'
		self.regmethod = switcher.get(reg, switcher[search_mount(reg)])

	def __main__(self, commands):
		pass




#https://safebrowsing.googleapis.com/v4/...?key=API_KEY
#d0940ab8-4f1b-495f-afe7-461e28b54aac

#f9e7209668feeba9cb5ed8960a6a5987df77f130bc4571c3db162e89bba34d9e virustotal
#api_key = "AIzaSyBlwFpAPBLHJTfzA1dk0B2MMdnGjvQPXQA"
#safebrowsing_config = SafeBrowsing(api_key)
#r = safebrowsing_config.lookup_urls(['http://ianfette.org'])

"""urls = 'customsearch'
version = 'v1'
service = build(urls, version, developerKey=api_key).cse()
pages = []
for i in range(1, 60, 10):
	result = service.list(q="python", cx="e13e6bab6d2274321", start=i).execute()
	pages += result['items']
print(len(pages))"""

