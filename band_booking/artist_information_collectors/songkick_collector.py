import urllib.request
import json
import threading
from math import ceil


# The api key
api_key = 'io09K9l3ebJxmxe2'


def get_past_events(artist_name):
    """
    Finds the past events of an artist by its name. Returns an error if no events can be found in Norway
    """
    artist_id = get_artist_id(artist_name.replace(" ", ""))
    if artist_id is None:
        return {'error': 'Could not find earlier events'}
    return get_past_events_by_id(artist_id)


def get_artist_id(artist_name):
    """
    Finds the id of the artist given its name.
    """
    results_json = load_request('http://api.songkick.com/api/3.0/search/artists.json?query=' + artist_name + '&')
    if results_json['totalEntries'] == 0:
        return None
    return results_json['results']['artist'][0]['id']


def get_past_events_by_id(artist_id):
    """
    Finds the past events of an artist by its id. Returns an error if no events can be found in Norway
    """
    results_json = load_request('http://api.songkick.com/api/3.0/artists/' + str(artist_id) + '/gigography.json?order=desc&page=1&')
    if results_json['totalEntries'] == 0:
        return {'error': 'Could not find earlier events'}
    events_norway = get_events_country("Norway", results_json['results']['event'])
    pages = ceil(results_json['totalEntries']/50)
    events = [events_norway] + [[]] * (pages - 1)
    threads = []

    for page in range(2, pages + 1):
        thread = PastEvents(artist_id, page, events)
        thread.run()
        threads.append(thread)

    while len(threads):
        for thread in threads:
            if not thread.isAlive():
                threads.remove(thread)

    events = build_events(events)

    if len(events) == 0:
        return {'error': 'Could not find earlier events'}
    return {'events': events}


def load_request(url):
    """
    Retrieves json from the given url, by appending the api key to the url, loading the url and decoding the result
    """
    results = urllib.request.urlopen(url + 'apikey=' + api_key).read()
    return json.loads(results.decode('UTF-8'))['resultsPage']


def get_events_country(country_code, event_json):
    """
    Filters the events on the given country code
    """
    return [event for event in event_json if event['venue']['metroArea']['country']['displayName'] == country_code]


def build_events(events):
    """
    Retrieves the appropriate information from all events
    """
    event_list = []
    for current_event_list in events:
        event_list += current_event_list
    return [build_event(event) for event in event_list]


def build_event(event):
    """
    Retrieves the appropriate information from an event
    """
    return {
        'name': event['displayName'].split("(")[0],
        'date': event['start']['date'],
        'city': event['location']['city'].split(",")[0]
    }


class PastEvents(threading.Thread):
    """
    Finds all events in norway for the given artist at the given page
    """

    def __init__(self, artist_id, page, events):
        super().__init__()
        self.artist_id = artist_id
        self.page = page
        self.events = events

    def run(self):
        result_json = load_request('http://api.songkick.com/api/3.0/artists/' + str(self.artist_id) + '/gigography.json?order=desc&page=' + str(self.page) + '&')
        self.events[self.page - 1] = get_events_country("Norway", result_json['results']['event'])