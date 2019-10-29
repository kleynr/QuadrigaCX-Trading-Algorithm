from time import sleep, time
from quadrigacx import quadrigacx
import arbitrage
import LOG
from mail import send
import managment
import json
#Position:{0 buy, 1 sell} | funds: $, Fee: %, ArbComplexity: {0 None, 1 Simple, 2 Complex} >>>> if in trade amount in market if not in trade amount to be played
class runner:
	def __init__(self, funds = 200, fee = 0.005):
		self.TradeLog, self.partialLog, self.nTrade, self.timeLog = {}, {}, 0, {}
		self.ask_dd = 0
		#parameters
		self.position, self.intrade, self.stat, self.funds, self.fee, self.fee1 = 0, 0, 0, funds, fee, 1-fee
		self.fee2 = self.fee1**2
		#libs
		self.sleep, self.QCX, self.managment, self.LOG, self.send = sleep, quadrigacx(), managment, LOG, send
		#Algo Runner
		self.run()

	def run(self):
		n = 0
		while True:
			try:
				starttime = time()
				#update | check order status | intrade
				arbitrage.update(self)
				self.managment.status(self)
				#default
				if self.intrade:

					CurrentTrade = self.TradeLog[self.id]
					self.sigDif = self.minAskd * self.fee
					#asking positon rember
					if self.ask_dd != 0:
						self.askp = round(self.askl[self.ask_dd]-0.01,2)
					self.minAsk = self.minAskd
				#print screen
				print('B/A/Min',self.bidp, self.askp, self.minAsk,'| regular min:', (self.bidl[self.bpos]+0.03)/self.fee2,
					'\nintrade:', self.intrade,
					'\narb: ', self.arbcomp,
					'\nsigDif:', self.sigDif,
					'\nbpos:', self.bpos,
					'\ncad,', self.cmc_CAD, float(self.cmc_CAD)*1.005,
					'\n','\033[4m','position:', self.position,'\033[0m')
				#Buying
				if self.position == 0:
					#Buying | Not Intrade | Arb exists
					if self.intrade == 0 and self.arbcomp > 0 and self.askp > self.minAsk:
						self.managment.bidbuy(self)

					#Buying | Intrade | moved up - MOD to check for better spots???
					elif self.intrade == 1 and self.bidl[self.bposd] != self.bidpd and self.bidpd in self.bidl[0:self.bposd]:
						#dont cancel | update
						print(0, '\033[47m', 'cancel results:', self.bidb[self.bposd], [self.bidpd, self.amount], self.askp, self.minAskd, self.bposd, '\033[0m')
						self.bposd = [x[0] for x in enumerate(self.bidl[0:self.bposd]) if x[1] == self.bidpd][0]

					#Buying | Intrade | not in position|||or self.arbcompd != self.arbcomp)
					elif self.intrade == 1 and (self.bidl[self.bposd] != self.bidpd):
						print('\033[47m', '1 cancel results:', self.bidb[self.bposd], [self.bidpd, self.amount], self.askp, self.minAskd, self.bposd, '\033[0m')
						self.QCX.cancel(self.id)

					#Buying | Intrade | FXarb --> askp low 
					elif self.intrade == 1 and (self.askp < self.minAskd or self.cmcFX(self) == 0):
						print('\033[47m', '2 cancel results:', self.askp, self.minAskd, self.cmcFX(self),'\033[0m')
						self.QCX.cancel(self.id)

					#Buying | Intrade | price below lower
					elif self.intrade == 1 and round(self.bidl[self.bposd+1]+0.01,2) < self.bidpd:
						print('\033[47m', '3 cancel results:', self.bidb[self.bposd], [self.bidpd, self.amount], self.askp, self.minAskd, self.bposd, '\033[0m')
						self.QCX.cancel(self.id)


				#Selling
				elif self.position == 1:
					#preset 
					askbelowp1 = round(self.askl[self.aposd+1]-0.01, 2)
					#Selling | Not Intrade | ask > min |ADD| if timetradechange > n and self.askp >= self.BEd
					if self.intrade == 0 and self.askp >= self.minAskd:
						self.managment.asksell(self)

					#Selling | Intrade | moved up ADD if down depending may not want to  lose pos depending
					elif self.intrade == 1 and self.askl[self.aposd] != self.askpd and self.askpd in self.askl[0:self.aposd]:
						#dont cancel | update
						self.aposd = [x[0] for x in enumerate(self.askl[0:self.aposd]) if x[1] == self.askpd][0]
						print(0, '\033[47m cancel sell \033[0m')

					#Selling | Intrade | not in position -> cancel OR Selling | Intrade | price below lowered
					elif self.intrade == 1 and self.askl[self.aposd] != self.askpd: 
						self.QCX.cancel(self.id)
						print('\033[47m 1 cancel sell \033[0m')

					#Selling | Intrade | not in position -> cancel OR Selling | Intrade | price below lowered
					elif self.intrade == 1 and askbelowp1 > self.askpd and self.askl[self.aposd+1] != self.askpd:
						 self.QCX.cancel(self.id)
						 print('\033[47m 2 cancel sell \033[0m')
				n += 1
				print('\033[4m', 'Time: ',time()-starttime,' || iterN: ', n,'\033[0m')
			
			except:
				#except (KeyError, ValueError, ConnectionError):
				print('--KeyError--')
				self.sleep(4)
				continue
runner()