import httplib
from urllib import urlencode
from json import loads


YOUR_API_KEY = ""

url = "cryptopay.me"

def create_invoice(price, **kwargs):
	""" Optional arguments and their defaults are
	currency='EUR', description=None id=None, callback_params=None, success_redirect_url=None, error_redirect_url=None, callback_url=None
	"""
	default_headers={'Content-Type': 'application/x-www-form-urlencoded'}
	kwargs['price'] = price

	h = httplib.HTTPSConnection(url)
	h.request("POST", "/api/v1/invoices?api_key=" + YOUR_API_KEY, urlencode(kwargs), default_headers)
	response = h.getresponse()
	
	if (response.status >= 200) and (response.status < 300):
		return loads(response.read())
	else:
		return "Server Error Code: " + str(response.status)  


if __name__ == "__main__":
	res = create_invoice(100, description="Test")
	print res

