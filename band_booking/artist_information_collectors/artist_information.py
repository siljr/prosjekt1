import discogs_client
import spotipy
from .songkick_collector import get_past_events


def find_artist(name):
    """
    Returns the first artist found at discogs and Spotify with the given name. If no items are found None is returned
    """
    artists_discogs = discogs.search(name, type='artist')
    artists_spotify = spotify.search(q='artist:' + name, type='artist')
    if len(artists_discogs) < 1 or len(artists_spotify['artists']['items']) == 0:
        return None, None
    artist_discogs = artists_discogs[0]
    artist_spotify = artists_spotify['artists']['items'][0]
    if not artist_discogs.name.startswith(artist_spotify['name']):
        return None, None
    return artist_discogs, artist_spotify


def get_artist_information(name):
    """
    Returns information about the given artist/band as a dictionary. If there is no valid artist,
    a dictionary with an error is returned.
    """
    artist_discogs, artist_spotify = find_artist(name)
    if artist_discogs is None:
        return {'error': 'Could not find information about the artist, ' + name}
    if is_band(artist_discogs):
        return build_band_information(artist_discogs, artist_spotify)
    return build_artist_information(artist_discogs, artist_spotify)


def build_base_information(artist_discogs, artist_spotify):
    """
    Builds the base information, that is valid in situations where the artist is a band or a single artist
    """
    return {
        'name': artist_discogs.name,
        'followers': artist_spotify['followers']['total'],
        'image': artist_spotify['images'][0],
        'albums': build_albums(artist_spotify),
        'past_events': get_past_events(artist_discogs.name)
    }


def build_band_information(band_discogs, band_spotify):
    """
    Builds information about a band
    """
    information = build_base_information(band_discogs, band_spotify)
    information['type'] = 'band'
    information['members'] = get_members(band_discogs)

    return information


def build_artist_information(artist_discogs, artist_spotify):
    """
    Builds information about an artist
    """
    information = build_base_information(artist_discogs, artist_spotify)
    information['type'] = 'artist'

    return information


def build_albums(artist_spotify):
    """
    Builds information about the last 5 albums made by the artist.
    """
    albums = spotify.artist_albums(artist_spotify['uri'], album_type='album', limit=10)['items']
    album_information = []
    album_names = []
    for album in albums:
        album = spotify.album(album['id'])
        
        if album['name'] in album_names:
            continue

        album_information.append({
            'image': album['images'][0],
            'name': album['name'],
            'tracks': build_track_information(album),
            'popularity': album['popularity']
        })
        album_names.append(album['name'])

        if len(album_names) == 5:
            break
    return album_information


def build_track_information(album):
    """
    Builds information about the tracks in a specific album
    """
    track_information = []
    for track in album['tracks']['items']:
        track_information.append({
            'name': track['name'],
            'track_number': track['track_number'],
            'duration': format_play_time(track['duration_ms'])
        })
    return track_information


def format_play_time(time):
    """
    Formats the time from milliseconds to a readable formatted string of HH:MM
    """
    time //= 1000
    return "%02d:%02d" % (time // 60, time % 60)


def get_members(band):
    """
    Returns the members of the band
    """
    return [artist.name for artist in band.members]


def is_band(artist):
    """
    Checks if the artist object is a band or an artist by checking if it has any members.
    Artists does not have any members, while bands have 2 or more members.
    """
    return len(artist.members) > 0


"""
Creates variables for access to the APIs.
"""
spotify = spotipy.Spotify()
discogs = discogs_client.Client('BandBooking/0.1', user_token='PPrabISUbdcQlOmgHRzQycSKBtCJuztKCFCQTbBe')
