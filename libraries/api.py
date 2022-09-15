# from errorhandler import FailedApi, HttpsError
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
class User_Agent:
	"""docstring for User_Agent"""
	def __init__(self, random):
		super(User_Agent, self).__init__()
		random.shuffle(user_agent_list)
		self.random = random
	def get(self):
		return self.random.choice(user_agent_list)
	def bot(self):
		return 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

class Api_Validate(object):
	def __init__(self, api, browser):
		super(Api_Validate, self).__init__()
		self.api = api
		if self.api is None or self.api == " ":
			self.show_error('empity')
		else:
			try:
				browsers = browser.get("https://google.com", timeout=2)
				if browsers.status_code == 200:
					self.api = browsers.status_code
				else:
					self.show_error('htp') 
			except:
				self.show_error('htp')

	def show_error(self, e):
		if e == "empity":
			raise Exception("API input")
		raise FailedApi("Failed API") or HttpsError("404")
			