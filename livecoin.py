#6XCE4FX58XZO6HCR
#HM3SYXI57Z0NQCSG
import requests
from time import time
def lcw():
	fxurl = 'http://webrates.truefx.com/rates/connect.html?f=html'
	url = 'https://www.livecoinwatch.com/price/Litecoin-LTC'
	cx = {'btc':'bitcoin','bch':'bitcoin-cash', 'btg':'bitcoin-gold','LTC':'Litecoin'}
	s, ss = '<div class="content colored">Price<div id="usd" class="sub header price colored">$', '</div>'
	FXdata = requests.get(fxurl).text
	data = requests.get(url).text
	p =  float(data.split(s)[1].split(ss)[0])
	d = FXdata.split('USD/CAD')[1].split('AUD/USD')[0].split('</td><td>')[2:6]
	b,a = float(d[0]+d[1]), float(d[2]+d[3]) 
	s = (b+a)*.5
	pCAD = p*s
	apCAD = pCAD
	print('livecoin', pCAD, apCAD)
	return pCAD, apCAD
lcw()