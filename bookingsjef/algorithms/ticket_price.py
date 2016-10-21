from band_booking.models import Scene
from band_booking.artist_information_collectors.artist_information import find_artist_spotify, get_popularity

__author__ = 'Weronika'


def get_ticket_prices_for_scenes(band_name, booking_price):
    """
    Returns list of lists [[Scene, price]] with ticket price suggestion for every scene.
    Returns None if band name is not found in Spotify
    """
    try:
        popularity = _get_avg_popularity(band_name)
        if popularity == 0:
            popularity = 1
    except ValueError:
        return None

    scenes = Scene.objects.all()
    info = []
    for scene in scenes:
        price = "{0:.2f}".format(_get_ticket_price_suggestion(scene, booking_price, popularity))
        info.append([scene, price])
    return info


def _get_marked_data(band_name):
    artist_spotify = find_artist_spotify(band_name)
    if artist_spotify is None:
        raise ValueError("No such band in Spotify")
    popularity = get_popularity(artist_spotify)
    return popularity


def _get_avg_popularity(band_name):
    popularity = _get_marked_data(band_name)
    return sum(popularity[:10]) / 10


def _get_minimum_ticket_price_to_cover_costs(scene: Scene, booking_price):
    return (scene.expenditure + booking_price) / scene.number_of_seats


def _get_ticket_price_suggestion(scene, booking_price, popularity):
    """
    Returns price suggestion for given scene. The more popular the band is, the higher the price and income
    """
    minimum_price = _get_minimum_ticket_price_to_cover_costs(scene, booking_price)
    return minimum_price * ((popularity / 200) + 1)
