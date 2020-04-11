import click

from .constants import DEFAULT_TRACK_COUNT


def generate_play_game_command(playlist_url, game_id, track_count, starting_track=None):
    cmd = "\tscripts/bingo.sh play-game --playlist=\"{}\" --game-id={}".format(playlist_url, game_id)

    if track_count != DEFAULT_TRACK_COUNT:
        cmd = "{} --track-count={}".format(cmd, track_count)

    if starting_track is not None:
        cmd = "{} --starting-track={}".format(cmd, starting_track)

    return cmd


class ClickLogger:
    def __init__(self, debug=False):
        self.debug = debug

    def log(self, message):
        click.echo(message)

    def log_track(self, track_no, total_tracks, name, artist):
        click.echo("Played {} of {}: {} - {}".format(track_no, total_tracks, name, artist))
