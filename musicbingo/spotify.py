import random
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

PLAYLIST_ID_RE = re.compile(r"https:\/\/open\.spotify\.com\/playlist\/([A-Za-z0-9]*).*")

class PlaylistDoesNotExist(Exception):
    pass


class SpotifyBingoPlaylist:
    def __init__(self, playlist_url):
        self.url = playlist_url
        self.id_ = self._get_playlist_id(playlist_url)

        scope = "user-read-playback-state,user-modify-playback-state"
        auth = SpotifyOAuth(username='mleonard87', redirect_uri='http://localhost', scope=scope)

        self.spotify_client = spotipy.Spotify(client_credentials_manager=auth)

        self._playlist = None
        self._tracks = None

        self._fetch_playlist()

    def _get_playlist_id(self, playlist_url):
        return PLAYLIST_ID_RE.findall(playlist_url)[0]

    def _fetch_playlist(self):
        if not self._playlist:
            try:
                self._playlist = self.spotify_client.playlist(self.id_)
            except spotipy.client.SpotifyException:
                raise PlaylistDoesNotExist()

        return self._playlist

    def name(self):
        playlist = self._fetch_playlist()
        return playlist['name']

    def _fetch_tracks(self):
        if not self._tracks:
            tracks = []
            page_size = 100
            counter = 0
            while True:
                offset = counter * page_size
                try:
                    page_tracks = self.spotify_client.playlist_tracks(
                        self.id_, offset=offset, limit=page_size)
                except spotipy.client.SpotifyException:
                    raise PlaylistDoesNotExist()


                for item in page_tracks['items']:
                    tracks.append(item)

                if not page_tracks['next']:
                    break

                counter += 1

            self._tracks = tracks

        return self._tracks

    def tracks(self, random_seed=None):
        api_tracks = self._fetch_tracks()

        if random_seed:
            random.seed(random_seed)
            random.shuffle(api_tracks)

        tracks = []
        for item in api_tracks:
            track = item['track']
            tracks.append({
                'name': track['name'],
                'artists': ', '.join([artist['name'] for artist in track['artists']]),
                'uri': track['uri'],
            })

        return tracks

    def get_card_tracks(self):
        return random.sample(self.tracks(), 24)

    def __str__(self):
        return str(self.data)

    def devices(self):
        return self.spotify_client.devices()['devices']

    def play(self, device_id, uri):
        self.spotify_client.start_playback(device_id=device_id, uris=[uri])

    def pause(self, device_id):
        self.spotify_client.pause_playback(device_id=device_id)
