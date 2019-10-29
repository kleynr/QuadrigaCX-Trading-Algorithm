from depth import simple, complexarb, biddepth, askdepth, sigdif, asksigdif
from CMC import cmc

def book(self):
	self.sleep(4)
	book = self.QCX.book()
	self.bidb, self.askb = [[float(bid),float(amount)] for bid,amount in book['bids']], [[float(ask),float(amount)] for ask,amount in book['asks']]
	self.bidl, self.askl = [b[0] for b in self.bidb], [a[0] for a in self.askb]
	self.bidp, self.askp = round(self.bidl[0]+.01,2), round(self.askl[0]-.01,2)
	#bidmath
	if self.position == 0 and self.intrade == 0:
		self.amount = self.funds/self.bidp
		self.managment.bidmath(self)
		self.sigDif = self.minAsk * self.fee

def arbitrage(self):
	#Buying  
	if self.position == 0 and self.intrade == 0:
		#if lowball/ large difference
		self.ask_d = 0
		if self.askp < self.minAsk: 
			self.ask_d = asksigdif(self)
			self.askp = round(self.askl[self.ask_d]-0.01,2)
		#Buying | SimpleArb | FX 
		if simple(self) == 1 and self.cmcFX(self) == 1: 
			self.bid_d = sigdif(self)
			self.bidstrength = [[s[0],s[1]] for s in enumerate(self.bidb) if s[1][1] > .55][0][0]
			if self.bidstrength > 0 or self.bid_d > 0: 
				self.bpos = max(self.bidstrength, self.bid_d, self.bpos)
				self.bidp = round(self.bidl[self.bpos]+.01,2)
				self.amount = self.funds/self.bidp
				self.managment.bidmath(self)
			self.arbcomp = 1
		#Buying | ComplexArb | Depth | FX
		elif complexarb(self) == 2 and biddepth(self) > 0:
			self.bpos = max(self.bpos2, self.bpos)
			self.bidp = round(self.bidl[self.bpos]+.01,2)
			if self.cmcFX(self) == 1:
				self.amount = self.funds/self.bidp
				self.managment.bidmath(self)
				self.arbcomp = 2

	#Selling 
	elif self.position == 1: 
		self.askstrength = [[s[0],s[1]] for s in enumerate(self.askb) if s[1][1] > 1][0][0]
		if self.askstrength > 0:
				self.apos = self.askstrength
				self.askp = round(self.askl[self.apos]-0.01,2)

		#if arb gone protocall
		if self.intrade == 0 and self.askp < self.minAskd:
			self.apos = [n for n in enumerate(self.askl) if n[1]-0.01 > self.minAskd][0][0]
			self.askp = round(self.askl[self.apos]-0.01,2)

def update(self):
	#default
	self.arbcomp, self.bpos, self.apos = 0, 0, 0
	#default to be set
	try: self.aposd
	except: self.aposd = 0
	
	try: self.bposd
	except: self.bposd = 0
	#run
	book(self)
	self.cmcFX = cmc
	arbitrage(self)