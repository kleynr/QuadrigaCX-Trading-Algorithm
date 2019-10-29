import requests
from time import time
from livecoin import lcw
###public - api get
url = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert=CAD'
cx = {'btc':'bitcoin','bch':'bitcoin-cash', 'btg':'bitcoin-gold','ltc':'litecoin'}

def FXcoinmarketcap(self):
	#and askp >= 1.03
	if self.intrade == 1 and self.position == 0:
		self.bidp = self.bidl[self.bposd]
	pCAD, pCADU = lcw()
	self.datacmc = requests.get(url.format(self.cx)).json()[0]
	self.cmc_CAD, self.cmc_USD = self.datacmc['price_cad'], self.datacmc['price_usd']
	self.FXarb = 0
	#1.0125
	if float(self.cmc_CAD)*1 >= self.bidp and pCAD*1>= self.bidp:
		self.FXarb = 1
	return self.FXarb

def cmc(self, coin = 'ltc'):
	self.coin, self.cx = coin, cx[coin]
	return FXcoinmarketcap(self)