class ResponseTx(object):
	def __init__(self, txid, data, mimetype, charset, filename):
		self.txid = txid
		self.data = data
		self.mimetype = mimetype
		self.charset = charset
		self.filename = filename
