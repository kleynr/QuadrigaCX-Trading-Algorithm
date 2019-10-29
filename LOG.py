import sqlite3
def log(self):
	#main db
	if self.id not in self.TradeLog:
		self.TradeLog[self.id] = {'funds':self.funds, 'position':self.position}
	#partial log
	elif len(self.partialLog) == 0:
		self.partamount = self.amountd
		if self.amountd != self.amount:
			self.partamount = self.amountd - self.amount
		self.partialLog[0] = {'price':self.mktprice,'amount':self.partamount, 'amountd':self.amountd}
	elif len(self.partialLog) > 0:
		#assume complete else
		self.partamount = self.amount
		if self.stat != 2:
			PART = sum([self.partialLog[x]['amount'] for x in self.partialLog if self.partialLog[x]['amountd'] == self.amountd])+self.amount
			self.partamount = self.amountd - PART
		self.partialLog[len(self.partialLog)] = {'price':self.mktprice, 'amount':self.partamount, 'amountd':self.amountd}
	print('TL:',self.TradeLog[self.id])
	print('PL:',self.partialLog)