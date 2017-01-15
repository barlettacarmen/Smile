 #       ___
 #      /   /\
 #     /___/  \
 #     \___\  /_      \_\_\_
 #    /   /\\/ /|    \_
 #   /___/  \_/ |   \_\_\_    \_ \_   \_  \_     \_\_\_
 #   \   \  / \ |        \_  \_\_\_  \_  \_     \_\_
 #    \___\//\_\|  \_\_\_   \_   \_ \_  \_\_\_ \_\_\_
 #     /___/  \
 #     \   \  /
 #      \___\/
 #
 # Copyright 2017 Fabiola Casasopra, Carmen Barletta, Gabriele Iannone, Guido Lanfranchi, Francesco Maio
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 # 	http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.







from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import string
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

import datetime
import webbrowser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def calend():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=calculatetill(), maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(deltat(event))
        print(start, event['summary'])
    return events

def calculatetill():
	nowt= datetime.datetime.now()
	delta = datetime.timedelta(hours = 2)
	t = nowt.time()
	h=(datetime.datetime.combine(datetime.date(1,1,1),t) + delta).time()

	till=str(datetime.datetime.now().date())+"T"+str(h)+"Z"

	return till


def selectmyplaylist(eventdesc):
	keyvalues=[["focus","study","lesson","lecture","concentration"],
			["party","disco","fun","aperitivo","birthday","compleanno"],
			["dinner","food","restaurant","pizza","lunch"],
			["sleep"],
			["workout", "sport","run","gym"],
			["chill","break", "relax"],
			["travel","flight", "train"]]

			
	
	s=eventdesc.lower()
	numcategories=7
	v=-1 # v rappresenta la posizione della prima lettera per la quale esiste un match nella frase 
	for i in range(numcategories):
		if v!=-1:
			break
		for k in keyvalues[i]:
			v=s.find(k)
			if v!=-1:
				eventid=keyvalues[i][0]
				break 
	print (v)

	client_credentials_manager = SpotifyClientCredentials()
	spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	if v!=-1:
		results = spotify.category_playlists(category_id=eventid,country='IT',limit=50,offset=0)
		selectedpl=random.randint(0,20)
		print (results["playlists"]["items"][selectedpl]["name"])
		url=results["playlists"]["items"][selectedpl]["external_urls"]["spotify"]
		print (url)
		webbrowser.open(url)
		return eventid
	else:
		results = spotify.category_playlists(category_id="break",country='IT',limit=50,offset=0)
		selectedpl=random.randint(0,20)
		print (results["playlists"]["items"][selectedpl]["name"])
		url=results["playlists"]["items"][selectedpl]["external_urls"]["spotify"]
		print (url)
		webbrowser.open(url)
		return "nomatch"




def lookForEvent():
    events=calend()
    if events:
    	return selectmyplaylist(events[0]['summary'])
    else:
    	return "noevent"

  