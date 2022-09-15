import requests, base64, hashlib, re
from Crypto import Random
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

class AESCipher:

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



class ScanHeaders:
	def __init__(self, url):
		self.url = url
		response = requests.get(self.url)
		self.text = response.content
		self.headers = response.headers
		self.cookies = response.cookies
		self.score = int(self.Point_Header()*4)

	def Point_Header(self):
		point = 0
		scann = [	self.scan_xxss(), self.scan_nosniff(), self.scan_xframe(), 
					self.scan_hsts(), self.scan_policy()]
		for x in scann:
			if x == 'get':
				point += 5
		return int(point)

	def scan_xxss(self):
		"""config failure if X-XSS-Protection header is not present"""
		xss = 'fail'	
		try:
			if self.headers["X-XSS-Protection"]:
				print("[+]", "X-XSS-Protection", ':', "pass")
				xss = 'get'
		except KeyError:
			print("[-]", "X-XSS-Protection header not present", ':', "fail!")
		return xss

	def scan_nosniff(self):
		"""X-Content-Type-Options should be set to 'nosniff' """
		x_content = 'fail'
		try:
			if self.headers["X-Content-Type-Options"].lower() == "nosniff":
				print("[+]", "X-Content-Type-Options", ':', "pass")
				x_content = 'get'
			else:
				print("[-]", "X-Content-Type-Options header not set correctly", ':', "fail!")
		except KeyError:
			print("[-]", "X-Content-Type-Options header not present", ':', "fail!")
		return x_content

	def scan_xframe(self):
		"""X-Frame-Options should be set to DENY or SAMEORIGIN"""
		x_frame = 'fail'
		try:
			if "deny" in self.headers["X-Frame-Options"].lower():
				print("[+]", "X-Frame-Options", ':', "pass")
				x_frame = "get"
			elif "sameorigin" in self.headers["X-Frame-Options"].lower():
				print("[+]", "X-Frame-Options", ':', "pass")
				x_frame = "get"
			else:
				print("[-]", "X-Frame-Options header not set correctly", ':', "fail!")
		except KeyError:
			print("[-]", "X-Frame-Options header not present", ':', "fail!")
		return x_frame

	def scan_hsts(self):
		"""config failure if HSTS header is not present"""
		stric_sec = 'fail'
		try:
			if self.headers["Strict-Transport-Security"]:
				print("[+]", "Strict-Transport-Security", ':', "pass")
				stric_sec = 'get'
		except KeyError:
			print("[-]", "Strict-Transport-Security header not present", ':', "fail!")
		return stric_sec

	def scan_policy(self):
		"""config failure if Security Policy header is not present"""
		content_sec_police = 'fail'
		try:
			if self.headers["Content-Security-Policy"]:
				print("[+]", "Content-Security-Policy", ':', "pass")
				content_sec_police= 'get'
		except KeyError:
			print("[-]", "Content-Security-Policy header not present", ':', "fail!")
		return content_sec_police

	def scan_secure(self, cookie):
		"""Set-Cookie header should have the secure attribute set"""
		cookies_set = 'fail'
		if cookie.secure:
			print("[+]", "Secure", ':', "pass")
			cookies_set = 'get'
		else:
			print("[-]", "Secure attribute not set", ':', "fail!")
		return cookies_set

	def scan_httponly(self, cookie):
		"""Set-Cookie header should have the HttpOnly attribute set"""
		httponly = 'fail'
		if cookie.has_nonstandard_attr('httponly') or cookie.has_nonstandard_attr('HttpOnly'):
			print("[+]", "HttpOnly", ':', "pass")
			httponly = 'get'
		else:
			print("[-]", "HttpOnly attribute not set", ':', "fail!")
		return httponly

	def scan_WindowPop(self):
		soup = BeautifulSoup(self.text, "html.parser")
		all_scripts = soup.find('script').prettify()
		window = re.search(r"window.location", all_scripts)
		window2 = re.search(r"window.open", all_scripts)
		jquery = re.search(r"$(location).attr", all_scripts)

		confirm1 = re.search(r"window.confirm", all_scripts)
		prompt = re.search(r"window.prompt", all_scripts)

		scan_WindowPop = 'fail'
		if window or window2 or jquery or confirm1 or prompt:
			scan_WindowPop = 'get'
		
		return scan_WindowPop
		


#if __name__ == "__main__":
	#target = ScanHeaders("http://127.0.0.1:5000/")
	#print(target.score)
	#for key in target.headers:
	#	print(key, ":", target.headers[key])
