import urllib.request
import json


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
    results_json = load_request('http://api.songkick.com/api/3.0/artists/' + str(artist_id) + '/gigography.json?order=desc&')
    if results_json['totalEntries'] == 0:
        return {'error': 'Could not find earlier events'}
    events_norway = get_events_country("Norway", results_json['results']['event'])
    if len(events_norway) == 0:
        return {'error': 'Could not find earlier events'}
    return {'events': build_events(events_norway)}


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
    return [build_event(event) for event in events]


def build_event(event):
    return {
        'name': event['displayName'],
        'date': event['start']['date'],
        'city': event['location']['city'].split(",")[0]
    }