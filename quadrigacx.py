import hashlib
import hmac
import requests
from time import time
#public - api get
url_ticker = 'https://api.quadrigacx.com/v2/ticker?book={}'
url_book = 'https://api.quadrigacx.com/v2/order_book?book={}'
url_transc = 'https://api.quadrigacx.com/v2/transactions?book={}'
#private - api post
url_bal = 'https://api.quadrigacx.com/v2/balance'
url_utransc = 'https://api.quadrigacx.com/v2/user_transactions'
url_open = 'https://api.quadrigacx.com/v2/open_orders'
url_lookup = 'https://api.quadrigacx.com/v2/lookup_order'
url_cancel = 'https://api.quadrigacx.com/v2/cancel_order'
url_buy = 'https://api.quadrigacx.com/v2/buy'
url_sell = 'https://api.quadrigacx.com/v2/sell'

class quadrigacx:
	def __init__(self, cx = 'ltc_cad', clientid = '', apikey = '', apisecret = ''):
		self.clientid, self.apikey, self.apisecret, self.cx = str(clientid), apikey, apisecret, cx

	#Nonce and Signature
	def signature(self):
		#uses ms for nonce to avoid collision
		nonce = str(int(time()*1000))
		msg = nonce+self.clientid+self.apikey
		signature = hmac.new(self.apisecret.encode(), msg=msg.encode(), digestmod=hashlib.sha256).hexdigest()
		return signature, nonce

	#public api 
	def ticker(self):
		response = requests.get(url_ticker.format(self.cx)).json()
		return self.handle_response(response)

	def book(self):
		response = requests.get(url_book.format(self.cx)).json()
		return self.handle_response(response)
		
	def transactions(self):
		response = requests.get(url_transc.format(self.cx)).json()
		return self.handle_response(response)

	#private api req. sign-in
	def balance(self):
		signature, nonce = self.signature()
		response = requests.post(url_bal, data={'key':self.apikey,'signature':signature,'nonce':nonce}).json()
		return self.handle_response(response)

	def open(self):
		signature, nonce = self.signature()
		response = requests.post(url_open, data={'key':self.apikey,'signature':signature,'nonce':nonce, 'book':self.cx}).json()
		return self.handle_response(response)

	def utransactions(self):
		signature, nonce = self.signature()
		response = requests.post(url_utransc, data={'key':self.apikey,'signature':signature,'nonce':nonce, 'book':self.cx}).json()
		return self.handle_response(response)

	def lookup(self, orderid):
		signature, nonce = self.signature()
		response = requests.post(url_lookup, data={'key':self.apikey,'signature':signature,'nonce':nonce, 'id':orderid}).json()
		return self.handle_response(response)

	#Market Actions
	def cancel(self, orderid):
		signature, nonce = self.signature()
		response = requests.post(url_cancel, data={'key':self.apikey,'signature':signature,'nonce':nonce, 'id':orderid}).json()
		return self.handle_response(response)

	def buy(self, amount, price):
		signature, nonce = self.signature()
		response = requests.post(url_buy, data={'key':self.apikey,'signature':signature,'nonce':nonce,
					'amount':amount,'price':price,'book':self.cx}).json()
		return self.handle_response(response)

	def sell(self, amount, price):
		signature, nonce = self.signature()
		response = requests.post(url_sell, data={'key':self.apikey,'signature':signature,'nonce':nonce,
					'amount':amount,'price':price,'book':self.cx}).json()
		return self.handle_response(response)

	def handle_response(self, response):
		return response