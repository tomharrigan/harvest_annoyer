import json, sched, time
import requests
from urlparse import urlparse
from base64   import b64encode as enc64

class Harvest(object):
	def __init__(self, uri="your harvest URL", email="your harvest email", password="your harvest password", ifttt_key="yourIFTTT Maker Channel key", ifttt_event="ifttt event prefix", num_events=3, frequency=300):
		self.__uri = uri.rstrip('/')
		parsed = urlparse(uri)
		if not (parsed.scheme and parsed.netloc):
			raise HarvestError('Invalid harvest uri "{0}".'.format(uri))

		self.__headers = {
			'Content-Type'  : 'application/json',
			'Accept'        : 'application/json',
			'User-Agent'    : 'Mozilla/5.0',  # 'TimeTracker for Linux' -- ++ << >>
		}

		self.__auth     = 'Basic'
		self.__email    = email.strip()
		self.__password = password
		self.__headers['Authorization'] = 'Basic {0}'.format(enc64('{self.email}:{self.password}'.format(self=self)))

		self.__ifttt_key = ifttt_key
		self.__ifttt_event = ifttt_event
		self.__num_events = num_events
		self.__frequency = frequency

	@property
	def uri(self):
		return self.__uri

	@property
	def auth(self):
		return self.__auth

	@property
	def email(self):
		return self.__email

	@property
	def password(self):
		return self.__password

	@property
	def client_id(self):
		return self.__client_id

	@property
	def ifttt_key(self):
		return self.__ifttt_key

	@property
	def ifttt_event(self):
		return self.__ifttt_event

	@property
	def num_events(self):
		return self.__num_events

	@property
	def frequency(self):
		return self.__frequency

	## Accounts

	@property
	def who_am_i(self):
		return self._get('/account/who_am_i')

	## Time Tracking

	@property
	def today(self):
		return self._get('/daily?slim=1')

	def _get(self, path='/', data=None):
		return self._request('GET', path, data)

	def _request(self, method='GET', path='/', data=None):
		url = '{self.uri}{path}'.format(self=self, path=path)
		kwargs = {
			'method'  : method,
			'url'     : '{self.uri}{path}'.format(self=self, path=path),
			'headers' : self.__headers,
			'data'   : json.dumps(data),
		}

		requestor = requests
		if 'Authorization' not in self.__headers:
			kwargs['auth'] = (self.email, self.password)

		try:
			resp = requestor.request(**kwargs)
			if 'DELETE' not in method:
				try:
					return resp.json()
				except:
					return resp
			return resp
		except Exception, e:
			raise HarvestError(e)

	def begin_tracking(self):
		counter = 1;
		s = sched.scheduler(time.time, time.sleep)
		s.enter(self.frequency, 1, self.track_me, (s, counter))
		s.run()

	def track_me(self, scheduler, counter=1):
		entries = json.loads(json.dumps(self._get('/daily?slim=1')))
		timer_exists = False
		for entry in entries["day_entries"]:
			if 'timer_started_at' in entry:
				timer_exists = True
				break

		if not timer_exists:
			event = counter%self.num_events
			if event is 0:
				event = self.num_events
			ifttturl = "https://maker.ifttt.com/trigger/"+ self.ifttt_event + "_" + str(event) + "/with/key/"+ self.ifttt_key
			requests.get(ifttturl)
			counter = counter + 1
		else:
			counter = 1

		print counter

		scheduler.enter(self.frequency, 1, self.track_me, (scheduler, counter))

harvest = Harvest()
harvest.begin_tracking()
