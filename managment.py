###status - status of the order (-1 - canceled; 0 - active; 1 - partially filled; 2 - complete)
def bidbuy(self):
	r = False
	n = 0 
	while not r:
		self.amount = round(self.amount, 8)
		rs = self.QCX.buy(self.amount, self.bidp)
		print(rs)
		if 'error' not in rs:
			self.id = rs['id']
			self.LOG.log(self)
			self.bposd, self.bidpd, self.amountd, self.minAskd, self.BEd = self.bpos, self.bidp, self.amount, self.minAsk, self.BE
			self.arbcompd, self.ask_dd = self.arbcomp, self.ask_d
			print('\033[42m', '--pos--bpos:',self.bposd,'bidp:', self.bidpd,'amount:', self.amountd,'min:', self.minAskd, '\033[0m')
			self.intrade = 1
			r = True
			#self.send(self)
		elif 'below the minimum' in rs['error']['message']:
			self.funds = 1.13
			self.amount = self.funds/self.bidp
			
		elif rs['error']['code'] == 200:
			n += 1
			self.sleep(3*n)
	return r

def asksell(self):
	r = False
	n = 0
	while not r:
		self.amount = round(self.amount, 8)
		rs = self.QCX.sell(self.amount, self.askp)
		print(rs)
		if 'error' not in rs:
			self.id = rs['id']
			self.LOG.log(self)
			self.aposd, self.askpd, self.amountd = self.apos, self.askp, self.amount
			print('\033[43m','--pos--apos:', self.aposd, 'askp:', self.askpd, 'amount:',self.amountd, 'min:', self.minAskd, '\033[0m')
			self.intrade = 1
			r = True
			#self.send(self)
		elif rs['error']['code'] == 200:
			n += 1
			self.sleep(3*n)
	return r

def bidmath(self):
	#minask for partial orders
	#amount not int
	if int(self.amount) != float(self.amount):
		remainder = float(self.amount)-int(self.amount)
		number = int(self.amount)
		rweight = remainder/self.amount
		nweight = 1-rweight
		gainmin = (0.02*nweight)+((0.02/remainder)*rweight)
		self.minAsk = round((self.bidp+gainmin)/self.fee2, 2)
		if len(self.partialLog) > 0:
			t_am =  self.amount+sum([self.partialLog[n]['amount'] for n in self.partialLog])
			bp = (self.bidp*(self.amount/t_am))
			self.minAsk = (bp+sum([(self.partialLog[n]['amount']/t_am)*self.partialLog[n]['price'] for n in self.partialLog]))/self.fee2
			self.minAsk = round(self.minAsk, 2)
	#int amount
	else:
		self.minAsk = round((self.bidp+0.02)/self.fee2, 2)

def status(self):
	if self.intrade:
		look = self.QCX.lookup(self.id)[0]
		
		## Test REMOVE
		self.amount = round(self.amount,8)
		print(look)
		## Test REMOVE

		self.stat, ltype, lamount, lprice = int(look['status']), int(look['type']), float(look['amount']), float(look['price'])
		#completed buy --> sell [-fund]
		if self.stat == 2 and ltype == 0:
			self.mktprice = lprice
			self.LOG.log(self)
			self.funds = 0
			self.amount = sum([self.partialLog[n]['amount'] for n in self.partialLog])*self.fee1
			self.position, self.intrade = 1,0
			self.partialLog = {}
			print('\033[92m', 'completeBUY: amount', self.amount,  '\033[0m')

		#completed sell --> buy [+fund]
		elif self.stat == 2 and ltype == 1:
			self.mktprice = lprice
			self.LOG.log(self)
			self.funds = sum([self.partialLog[n]['amount']*self.partialLog[n]['price'] for n in self.partialLog])*self.fee1
			self.amount = 0
			self.position, self.intrade = 0,0
			self.partialLog = {}
			print('\033[93m', 'completeSELL: $', self.funds,  '\033[0m')

		#cancel pos --> pos cont. [-fund]
		elif self.stat == -1 and ltype == 0:
			if self.amountd != lamount:
				self.amount, self.mktprice = lamount, lprice
				self.LOG.log(self)
				self.funds -= self.mktprice*self.partamount
			self.intrade = 0

		#cancel pos --> pos cont. [+fund]
		elif self.stat == -1 and ltype == 1: 
			if self.amount != lamount:
				self.amount, self.mktprice = lamount, lprice
				self.LOG.log(self)
				self.funds += (self.mktprice*self.partamount)*self.fee1
			self.intrade = 0

		#partial pos --> cont. [-fund]
		elif self.stat == 1 and ltype == 0:
			if self.amount != lamount:
				self.amount, self.mktprice = lamount, lprice
				self.LOG.log(self)
				self.funds -= self.mktprice*self.partamount

		#partial pos --> cont. [+fund]
		elif self.stat == 1 and ltype == 1:
			if self.amount != lamount:
				self.amount, self.mktprice = lamount, lprice
				self.LOG.log(self)
				self.funds += (self.mktprice*self.partamount)*self.fee1