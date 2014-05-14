import unittest
from ARClient import ARClient

class TestARClient(unittest.TestCase):
	def setUp(self):
		global host, key, secret
		self.client = ARClient(apiHost = host, key = key, secret = secret)
		self.client.init()
		
	def test_echo(self):
		self.assertEqual(self.client.doRequest('/api/echo', {'echo': 'test'})['data'], 'test')

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Test cases for ARClient library.')
	parser.add_argument("--host", required=True)
	parser.add_argument("--key", required=True)
	parser.add_argument("--secret", required=True)
	
	arguments = parser.parse_args()
	host = arguments.host
	key = arguments.key
	secret = arguments.secret
	
	suite = unittest.TestLoader().loadTestsFromTestCase(TestARClient)
	unittest.TextTestRunner().run(suite)