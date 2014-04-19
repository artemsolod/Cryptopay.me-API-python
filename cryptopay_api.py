from __future__ import print_function
import httplib
from urllib import urlencode
from json import loads



YOUR_API_KEY = ""

url = "cryptopay.me"

def get_balance():
	return basic_request("/balance", with_token=True)

def basic_request(req_path, args_dict={}, with_token=False, req_type="GET"):
	default_headers={'Content-Type': 'application/x-www-form-urlencoded'}
	h = httplib.HTTPSConnection(url)
	if with_token:
		args_dict["api_key"] = YOUR_API_KEY
	h.request(req_type, "/api/v1" + req_path, urlencode(args_dict), default_headers)
	response = h.getresponse()
	if (200 <= response.status < 300):
		return loads(response.read())
	else:
		return "Server Error Code: " + str(response.status)

def create_invoice(price, **kwargs):
	""" Optional arguments and their defaults are
	currency='EUR', description=None id=None, callback_url=None, callback_params=None, success_redirect_url=None, confirmations_count=4
	"""
	kwargs['price'] = price
	req_path = "/invoices"
	return basic_request(req_path, kwargs, True, "POST")

def view_invoice(uuid):
	req_path = "/invoices/" + str(uuid)
	return basic_request(req_path, with_token=True, req_type="GET")

def requote(uuid):
	req_path = "/invoices/" + str(uuid)
	return basic_request(req_path, with_token=True, req_type="PUT")

def list_invoices(page_number=1, per_page=20, from_time=None, to_time=None):
	args_dict= {}
	args_dict['per_page'] = per_page
	args_dict['page_number'] = page_number
	args_dict['from'] = from_time
	args_dict['to_time'] = to_time
	req_path = "/invoices/"
	return basic_request(req_path, with_token=True, req_type="GET")


if __name__ == "__main__":
	# res = create_invoice(100, description="Test")
	# res = requote("19c80fd8-8401-45f3-83f0-33f48c0091ed")
	res = list_invoices()
	print(res)
# 07e13fce-ff9c-4ccb-b34d-8e26562e4b46
# {u'status': u'pending', u'btc_price': u'0.2805', u'valid_till': 1397926143, u'callback_url': None, u'success_redirect_url': None, u'uuid': u'19c80fd8-8401-45f3-83f0-33f48c0091ed', u'short_id': u'19C80FD8', u'confirmations_count': 1, u'url': u'http://cryptopay.me/orders/19c80fd8-8401-45f3-83f0-33f48c0091ed/d', u'price': 100.0, u'currency': u'EUR', u'callback_params': None, u'bitcoin_uri': u'bitcoin:1ARVioYH5cxwFYffmNmNkWEfzmbcGxN6k4?amount=0.2805', u'created_at': 1397925543, u'btc_address': u'1ARVioYH5cxwFYffmNmNkWEfzmbcGxN6k4', u'id': None, u'description': u'Test'}