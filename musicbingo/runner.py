import click

from .spotify import SpotifyBingoPlaylist, PlaylistDoesNotExist
from .card import MusicBingoCard
from .game import MusicBingo

import random
import time


class ClickLogger:
    @staticmethod
    def log(message):
        click.echo(message)


@click.group()
def cli():
    pass

@click.command()
@click.option('--playlist', help='The Spotify playlist URL to use.')
@click.option('--cards', default=1, help='Number of bingo cards to make.')
def generate_cards(playlist, cards):
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

    for i in range(cards):
        card = MusicBingoCard(bingo_playlist, i+1)
        card.write()


@click.command()
@click.option('--playlist', help='The Spotify playlist URL to use.')
@click.option('--game-id', default=None, help='A game ID to resume playing')
@click.option('--clip-duration', default=30, help='How long should the song clip play for?')
@click.option('--starting-track', default=0, help='The track number to start from. Useful with --game-id for resuming a game.')
@click.option('--verbose', '-v', is_flag=True, help='Whether or not to display the tracks once they have been played.')
def play_game(playlist, game_id, clip_duration, starting_track, verbose):
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

    logger = None
    if verbose:
        logger = ClickLogger()

    game = MusicBingo(bingo_playlist, device_id, clip_duration, game_id, starting_track, logger)
    click.secho(
        "To resume this game with the tracks in the same order pass the flag --game-id {}".format(game.game_id),
        fg='green')

    try:
        game.start()
    except KeyboardInterrupt:
        game.stop()
        click.secho(
            "To resume the game where you left off run with --game-id {} --starting-track {}".format(game.game_id, game.current_track - 1),  # minus 1 because we already advanced it
            fg='green'
        )

    if game.end_status == 'PLAYLIST_COMPLETE':
        click.secho(
            "Game ended. All tracks have been played.",
            fg='yellow'
        )

cli.add_command(generate_cards)
cli.add_command(play_game)

if __name__ == '__main__':
    cli()
