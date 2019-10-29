from numpy import diff, absolute
def simple(self):
	self.arbcompSimple = 0
	self.BE = round(self.bidp/self.fee2, 2)
	if self.askp >= self.minAsk:
		self.arbcompSimple = 1
	return self.arbcompSimple

def complexarb(self):
	self.arbcompComplex = 0
	ucombo = []
	asks = self.askl[0:10]
	bids = self.bidl[0:10]
	ucombo = [[b+0.01,a-0.01] for b in bids for a in asks if (b,a) not in ucombo if (a,b) not in ucombo]
	self.plsim = [[d[0],d[1]] for d in enumerate(ucombo) if d[1][1]-d[1][0]-(((sum(d[1])+0.02)/self.fee1)-sum(d[1])) >= 0.01]
	if len(self.plsim) > 0:
		self.arbcompComplex = 2
		self.bpos2 = [n[0] for n in enumerate(bids) if round(self.plsim[0][1][0]-0.01, 2)  == n[1]][0]
	return self.arbcompComplex

def biddepth(self):
	bidd = absolute(diff(self.bidl[0:10]))
	n, bd = 0.01, list(enumerate(bidd[:]))
	while len(bd) >= 3:
		bd = [(i,d) for i,d in bd if d > n]
		n += 0.01
	if len(bd) > 0: 
		self.bpos = bd[0][0] + 1
	return self.bpos

def askdepth(self):
	#finish for ask
	askd = absolute(diff(self.askl[0:10]))
	n, ad = 0.01, list(enumerate(askd[:]))
	while len(ad) >= 3:
		ad = [(i,d) for i,d in ad if d > n]
		n += 0.01 
	if len(ad) > 0:
		self.apos = ad[0][0] + 1
	return self.apos

def sigdif(self):
	#make for ask or 5 instead
	self.bid_d = 0
	bid_d = [(i,d) for i,d in enumerate(absolute(diff(self.bidl[0:5]))) if self.sigDif < d]
	if len(bid_d) > 0:
		self.bid_d = bid_d[0][0] + 1
	return self.bid_d

def asksigdif(self):
	self.ask_d = 0
	ask_d = [(i,d) for i,d in enumerate(absolute(diff(self.askl[0:3]))) if self.sigDif < d]
	if len(ask_d) > 0:
		self.ask_d = ask_d[0][0] + 1
	return self.ask_d