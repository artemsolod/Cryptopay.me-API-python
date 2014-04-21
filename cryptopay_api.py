from __future__ import print_function
import httplib
from urllib import urlencode
from json import loads



YOUR_API_KEY = "c91336d748a4f1dc6589c1653bf6be37"

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

def create_button(price, currency=None, name=None):
	args_dict = {}
	args_dict['price'] = price
	args_dict['currency'] = currency
	args_dict['name'] = name
	req_path = "/buttons"
	return basic_request(req_path, args_dict, True, "POST")


if __name__ == "__main__":
	res = create_button(100, "GBP", "lol")
	print(res)
