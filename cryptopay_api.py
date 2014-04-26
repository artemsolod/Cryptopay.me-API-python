from __future__ import print_function
import httplib
import hashlib
from urllib import urlencode
from json import loads, dumps


YOUR_API_KEY = ""

url = "cryptopay.me"

def basic_request(req_path, args_dict={}, with_token=False, req_type="GET"):
	default_headers={'Content-Type': 'application/json'}
	h = httplib.HTTPSConnection(url)
	total_path = "/api/v1" + req_path + (("?api_key=" + YOUR_API_KEY) if with_token else "")
	h.request(req_type, total_path, dumps(args_dict), default_headers)
	response = h.getresponse()
	if (200 <= response.status < 300):
		return loads(response.read())
	else:
		return "Server Error Code: " + str(response.read()) # str(response.status)


def get_balance():
	return basic_request("/balance", with_token=True)

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
	args_dict['page'] = page_number
	if from_time: args_dict['from'] = from_time
	if to_time: args_dict['to'] = to_time
	req_path = "/invoices"
	return basic_request(req_path, args_dict, True, "GET")

def create_button(price, currency=None, name=None):
	args_dict = {}
	args_dict['price'] = price
	args_dict['currency'] = currency
	args_dict['name'] = name
	req_path = "/buttons"
	return basic_request(req_path, args_dict, True, "POST")

def create_hosted(items, **kwargs):
	kwargs['items'] = items
	req_path = "/hosted"
	return basic_request(req_path, kwargs, True, "POST")

def validate_hash(uuid, price, currency, test_hash):
	to_check = YOUR_API_KEY + '_' + uuid + '_' + str(int(price*100)) + currency
	computed_hash = hashlib.sha256(to_check).hexdigest()
	return (computed_hash == test_hash)



if __name__ == "__main__":
	its = [{"name": "lol", "price": 50, "quantity": 2, "vat_rate":10}]
	res = create_hosted(its)
	print(res)
