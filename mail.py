import smtplib

def send(self):
	TO = ''
	SUBJECT = 'TRADE ALERT SIGNAL - Pos: {} '.format(self.position)
	TEXT = 'Check --- Trade Placed\nMINprice: {}\namount: {}\nB/A: {},{}\n'.format(self.minAsk, self.amountd, self.bidp, self.askp)

	# Gmail Sign In (use non-primary account and allow to sign in with less secure apps)
	# tradenotfication or nxtgenco
	gmail_sender = ''
	gmail_passwd = ''

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(gmail_sender, gmail_passwd)

	BODY = '\r\n'.join(['To: %s' % TO, 'From: %s' % gmail_sender, 'Subject: %s' % SUBJECT, '', TEXT])

	try:
	    server.sendmail(gmail_sender, [TO], BODY)
	    print ('email sent')
	except:
	    print ('error sending mail')

	server.quit()