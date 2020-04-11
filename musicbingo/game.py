import asyncio
import random

from .card import MusicBingoCard


class MusicBingo:
    def __init__(self, playlist, game_id, track_count, device_id=None, clip_duration=None, duration_between_tracks=None, starting_track=0, logger=None):
        self.playlist = playlist
        self.game_id = game_id
        if not game_id:
            self.game_id = str(random.randint(0, 1000000))
        self.device_id = device_id
        self.clip_duration = clip_duration
        self.duration_between_tracks = duration_between_tracks
        self.current_track = starting_track
        self.logger = logger

        self.tracks = self.playlist.tracks(random_seed=self.game_id)[:track_count]

        if self.logger:
            for idx, track in enumerate(self.tracks):
                self.logger.log("{}: {} - {}".format(idx, track['name'], track['artists']))

        self._loop = asyncio.get_event_loop()

        self.end_status = None

    def generate_bingo_cards(self, players):
        try:
            player_count = int(players)
            cards = range(1, player_count+1)
        except ValueError:
            # Can't cast to an int so we will treat players as a CSV list of player names
            cards = players.split(',')

        for i in cards:
            card = MusicBingoCard(self.playlist.name(), self.tracks, i, self.game_id)
            card.write()

    def start(self):
        self.next_track()
        self._loop.run_forever()

    def next_track(self):
        try:
            # Note the -1's below because we want to log the previously played track
            if self.current_track > 0:
                track_info = self.tracks[self.current_track-1]
                self.logger.log_track(self.current_track, len(self.tracks),
                    track_info['name'], track_info['artists'])

            if self.current_track >= len(self.tracks):
                self.stop()
                self.end_status = 'PLAYLIST_COMPLETE'
                return

            track = self.tracks[self.current_track]
            uri = track['uri']

            self.playlist.play(self.device_id, uri)

            if self.duration_between_tracks > 0:
                 self._loop.call_later(self.clip_duration, self.pause_track)
                 self._loop.call_later(self.clip_duration + self.duration_between_tracks, self.next_track)
            else:
                self._loop.call_later(self.clip_duration, self.next_track)

            self.current_track = self.current_track + 1
        except:
            self.stop()
            raise

    def pause_track(self):
        self.playlist.pause(self.device_id)

    def stop(self):
        self.pause_track()
        self._loop.stop()

