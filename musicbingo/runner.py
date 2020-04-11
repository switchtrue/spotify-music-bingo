import click

from .constants import DEFAULT_TRACK_COUNT, DEFAULT_CLIP_DURATION, DEFAULT_DURATION_BETWEEN_CLIPS
from .spotify import SpotifyBingoPlaylist, PlaylistDoesNotExist
from .card import MusicBingoCard
from .game import MusicBingo
from .utils import generate_play_game_command, ClickLogger

import random
import time


@click.group()
def cli():
    pass

@click.command()
@click.option('--playlist', help='The Spotify playlist URL to use.')
@click.option('--game-id', default=None, help='A game ID to resume playing')
@click.option('--players', default="1", help='Number of bingo cards to make or a CSV list of player names.')
@click.option('--track-count', default=DEFAULT_TRACK_COUNT, help='The number of tracks to use from the playlist.')
@click.option('--debug', is_flag=True, default=False, help='Whether or not to output additional logging.')
def generate_cards(playlist, game_id, players, track_count, debug):
    try:
        bingo_playlist = SpotifyBingoPlaylist(playlist)
    except PlaylistDoesNotExist:
        click.secho(
            "ERROR: The specified playlist does not exist.", fg='red')
        return 1

    if len(bingo_playlist.tracks()) < 24:
        click.secho(
            "ERROR: Playlist is too short. Must have at least 24 tracks.", fg='red')
        return 1

    logger = ClickLogger(debug)

    game = MusicBingo(bingo_playlist, game_id, track_count, logger=logger)

    click.secho("To play this game with the same tracks in the same order:\n")
    click.secho(generate_play_game_command(playlist, game.game_id, track_count), fg="green")
    click.secho("\n")

    game.generate_bingo_cards(players)


@click.command()
@click.option('--playlist', help='The Spotify playlist URL to use.')
@click.option('--game-id', default=None, help='A game ID to resume playing')
@click.option('--clip-duration', default=DEFAULT_CLIP_DURATION, help='How long should the song clip play for?')
@click.option('--duration-between-clips', default=DEFAULT_DURATION_BETWEEN_CLIPS, help='The number of seconds of slience between clips')
@click.option('--starting-track', default=0, help='The track number to start from. Useful with --game-id for resuming a game.')
@click.option('--track-count', default=DEFAULT_TRACK_COUNT, help='The number of tracks to use from the playlist.')
@click.option('--debug', is_flag=True, default=False, help='Whether or not to output additional logging.')
def play_game(playlist, game_id, clip_duration, duration_between_clips, starting_track, track_count, debug):
    try:
        bingo_playlist = SpotifyBingoPlaylist(playlist)
    except PlaylistDoesNotExist:
        click.secho(
            "ERROR: The specified playlist does not exist.", fg='red')
        return 1

    devices = bingo_playlist.devices()
    if len(devices) > 1:
        for idx, device in enumerate(devices):
            click.secho(
                "{}: {}".format(idx, device['name']),
            )

        value = click.prompt('Enter a device number ({}-{}) to play on'.format(0, len(devices)-1), type=int)
        device_id = devices[value]['id']
    else:
        device_id = devices[0]['id']

    logger = ClickLogger(debug)

    click.secho("Using playlist {} with {} tracks.".format(bingo_playlist.name(), len(bingo_playlist.tracks())))

    game = MusicBingo(bingo_playlist, game_id, track_count, device_id, clip_duration, duration_between_clips, starting_track, logger)

    click.secho("To play this game with the same tracks in the same order:\n")
    click.secho(generate_play_game_command(playlist, game_id, track_count), fg="green")
    click.secho("\n")

    try:
        game.start()
    except KeyboardInterrupt:
        game.stop()
        click.secho("\nTo resume this game where you left off:\n")
        click.secho(
            generate_play_game_command(playlist, game_id, track_count, game.current_track - 1), # minus 1 because we already advanced it
            fg="green")
        click.secho("\n")

    if game.end_status == 'PLAYLIST_COMPLETE':
        click.secho(
            "Game ended. All tracks have been played.",
            fg='yellow'
        )

cli.add_command(generate_cards)
cli.add_command(play_game)

if __name__ == '__main__':
    cli()
