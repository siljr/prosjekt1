from band_booking.models import Scene
from band_booking.artist_information_collectors.artist_information import find_artist, get_popularity

__author__ = 'Weronika'


def get_ticket_prices_for_scenes(band_name, booking_price):
    scener = Scene.objects.all()
    info = []
    for scene in scener:
        info.append([scene, 10000])
    return info


def _get_marked_data(band_name):
    artist_dicogs, artist_spotify = find_artist(band_name)
    popularity = get_popularity(artist_spotify)
    avg_popularity = _get_avg_popularity(popularity)
    return avg_popularity


def _get_avg_popularity(popularity):
    return sum(popularity[:10]) / 10


def _get_minimum_ticket_price_to_cover_costs(scene: Scene, booking_price):
    return (scene.expenditure + booking_price) / scene.number_of_seats
