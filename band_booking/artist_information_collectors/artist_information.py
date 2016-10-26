import discogs_client
import spotipy


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
    if artist_discogs.name not in artist_spotify['name'] and artist_spotify['name'] not in artist_discogs.name:
        if artist_spotify['name'] == name:
            return None, artist_spotify
        return None, None
    return artist_discogs, artist_spotify


def find_artist_spotify(name):
    """
    Finds the artist with the given name on Spotify
    """
    artists_spotify = spotify.search(q='artist:' + name, type='artist')

    if len(artists_spotify['artists']['items']) == 0:
        return None

    artists_spotify = artists_spotify['artists']['items'][0]
    if artists_spotify['name'].lower() == name.lower() or artists_spotify['name'].lower().startswith(name.lower()):
        return artists_spotify

    return None


def get_artist_information(name):
    """
    Returns information about the given artist/band as a dictionary. If there is no valid artist,
    a dictionary with an error is returned.
    """
    artist_discogs, artist_spotify = find_artist(name)
    if artist_spotify is None:
        return {'error': 'Kunne ikke finne informasjon om ' + name}
    if artist_discogs is None:
        return build_artist_information(artist_spotify)
    if is_band(artist_discogs):
        return build_band_information(artist_discogs, artist_spotify)
    return build_artist_information(artist_spotify)


def build_base_information(artist_spotify):
    """
    Builds the base information, that is valid in situations where the artist is a band or a single artist
    """
    return {
        'name': artist_spotify['name'],
        'followers': artist_spotify['followers']['total'],
        'image': artist_spotify['images'][0],
        'albums': build_albums(artist_spotify),
    }


def build_band_information(band_discogs, band_spotify):
    """
    Builds information about a band
    """
    information = build_base_information(band_spotify)
    information['type'] = 'band'
    information['members'] = get_members(band_discogs)

    return information


def build_artist_information(artist_spotify):
    """
    Builds information about an artist
    """
    information = build_base_information(artist_spotify)
    information['type'] = 'artist'

    return information


def build_albums(artist_spotify):
    """
    Builds information about the last 5 albums made by the artist.
    """
    albums = spotify.artist_albums(artist_spotify['uri'], album_type='album', limit=30)['items']
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
            'popularity': album['popularity'],
            'sales': str(int((artist_spotify['followers']['total'] * album['popularity'])/57.13))
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
    return [artist.name.split("(")[0] for artist in band.members]


def is_band(artist):
    """
    Checks if the artist object is a band or an artist by checking if it has any members.
    Artists does not have any members, while bands have 2 or more members.
    """
    return len(artist.members) > 0


def get_popularity(artist_spotify):
    """
    Returns information about popularity of up to 50 bands albums.
    """
    albums = spotify.artist_albums(artist_spotify['uri'], album_type='album', limit=50)['items']
    popularity = []
    album_names = []
    for album in albums:
        album = spotify.album(album['id'])

        if album['name'] in album_names:
            continue
        popularity.append(int(album['popularity']))
        album_names.append(album['name'])

        if len(album_names) == 50:
            break
    popularity.sort(reverse=True)
    return popularity

"""
Creates variables for access to the APIs.
"""
spotify = spotipy.Spotify()
discogs = discogs_client.Client('BandBooking/0.1', user_token='PPrabISUbdcQlOmgHRzQycSKBtCJuztKCFCQTbBe')
