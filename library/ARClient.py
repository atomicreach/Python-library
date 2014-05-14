#! /usr/bin/env python
# coding: utf-8
"""
    ARClient
    ~~~~~~~~~~~~~

    Provides Access to the Atomic Reach API.

    :copyright: year, see AUTHORS for more details
    :license: license_name, see LICENSE for more details
"""

class ARClient:
	STATUS_OK = 10
	STATUS_INTERNAL_ERROR = 20
	STATUS_INVALID_ACCESS_TOKEN = 21
	STATUS_THRESHOLD_EXCEEDED = 22
	STATUS_INVALID_ACTION = 23
	STATUS_INVALID_DATA = 24
	import urllib
	import oauth2 as oauth

	def __init__(self, apiHost, key, secret):
		if None in (apiHost, key, secret):
			raise ValueError("Please provide all required parameters")

		import urlparse
		
		oauth = self.oauth
		self.consumer = consumer = oauth.Consumer(key=key, secret=secret)
		self.apiHost = apiHost
		client = oauth.Client(consumer)
		client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())

		#Request
		self.request_token_url = request_token_url = apiHost + '/oauth/request-token'
		resp, content = client.request(request_token_url, "GET")

		if resp['status'] != '200':
			raise Exception("Invalid response %s." % resp['status'])

		self.request_token = request_token = dict(urlparse.parse_qsl(content))

		#Authorize
		authorize_url = apiHost + '/oauth/authorize'
		request = oauth.Request(method = "GET", url=authorize_url, parameters = {'oauth_token': request_token['oauth_token']})
		client.request(request.to_url(), "GET")


	def init(self):
		import urlparse
		import json
		self.json = json
		access_token_url = self.apiHost + '/oauth/access-token'
		oauth = self.oauth
		#Get Access Token
		token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
		client = oauth.Client(self.consumer, token)
		client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())

		resp, content = client.request(access_token_url, "GET")

		access_token = dict(urlparse.parse_qsl(content))
		
		self.client = oauth.Client(self.consumer, oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret']))
		self.client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())

	def doRequest(self, url, params):
		try:
			try:
				body = self.urllib.urlencode(params)
			except ValueError:
				body = ''

			resp, content = self.client.request(self.apiHost + url, "POST", body = body)
			
			return self.json.loads(content)
		except AttributeError:
			raise NotInitialized("Make sure to call init() before calling any other method")

	def _doRequest(self, url, params):
		try:
			del params['self']
		except:
			pass
		for k, v in params.items():
			if v is None:
				del params[k]
		return self.doRequest(url, params)

	def addPost(self, text, teaser, sourceId, segmentId, title, pubDate, postUrl):
		"""Calls the post/add service."""
		return self._doRequest('/post/add', locals())

	def analyzePost(self, content, title = '', segmentId = None):
		"""Calls the post/analyze service."""
		return self._doRequest('/post/analyze', locals())

	def addSource(self, title, segmentDataJson):
		"""Calls the source/add service."""
		return self._doRequest('/source/add', locals()) 

	def getAudienceList(self):
		"""Calls the source/get-audience-list service."""
		return self._doRequest('/source/get-audience-list', {})

	def addDictionary(self, word):
		"""Calls the dictionary/add service."""
		return self._doRequest('/dictionary/add', locals())

	def removeDictionary(self, word):
		"""Calls the dictionary/remove service."""
		return self._doRequest('/dictionary/remove', locals())

	def listDictionaries(self):
		"""Calls the dictionary/list service."""
		return self._doRequest('/dictionary/list', {})

class NotInitialized(Exception):
	pass

