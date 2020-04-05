import asyncio
import random


class MusicBingo:
    def __init__(self, playlist, device_id, clip_duration, duration_between_tracks, game_id, starting_track=0, logger=None):
        self.playlist = playlist
        self.device_id = device_id
        self.clip_duration = clip_duration
        self.duration_between_tracks = duration_between_tracks
        self.game_id = game_id
        if not game_id:
            self.game_id = str(random.randint(0, 1000000))
        self.current_track = starting_track
        self.logger = logger

        self.tracks = self.playlist.tracks(random_seed=self.game_id)

        self._loop = asyncio.get_event_loop()

        self.end_status = None

    def start(self):
        self.next_track()
        self._loop.run_forever()

    def next_track(self):
        try:
            # Note the -1's below because we want to log the previously played track
            if self.logger and self.current_track > 0:
                track_info = self.tracks[self.current_track-1]
                self.logger.log('Played {} of {}: {} - {}'.format(
                    self.current_track, len(self.tracks), track_info['name'], track_info['artists']))

            if self.current_track >= len(self.tracks):
                self.stop()
                self.end_status = 'PLAYLIST_COMPLETE'
                return

            track = self.tracks[self.current_track]
            uri = track['uri']

            self.playlist.play(self.device_id, uri)

            if self.duration_between_tracks > 0:
                 self._loop.call_later(self.duration_between_tracks, self.pause_track)
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

