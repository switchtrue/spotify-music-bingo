import click

from .spotify import SpotifyBingoPlaylist, PlaylistDoesNotExist
from .card import MusicBingoCard



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


cli.add_command(generate_cards)

if __name__ == '__main__':
    cli()
