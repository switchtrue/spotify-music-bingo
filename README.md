# Spotify Music Bingo

Generate bing cards from a Spotify playlist and then play short clips of each song to play music
bingo.

# Installation

1. Clone this repository
2. pip install -r requirements.txt

# Usage

## Generate Bingo Cards

`scripts/bingo.sh generate-cards --playlist <playlist_url> --cards 5`

## Start a New Game

`scripts/bingo.sh play-game --playlist <playlist_url> [--clip-duration <seconds>] [--verbose]`

`--clip-duration` is optional and controls how much of the beginning of the track is played. The
default is 30 seconds.

`--verbose` will log each track after it has played.

## Resuming a Game

The order of the tracks played is randomised when a game is started. However, you can pass in a
`game id` that get used to seed the randomisation of the tracks. When a new game is started the
game id is displayed and can be passed back in with a starting track number to carry on where you
left off.

`scripts/bingo.sh play-game --playlist <playlist_url> --game-id <game_id> --starting-track <track_number> [--clip-duration <seconds>]`

When you exit a game the `--game-id` and `--starting-track` will be output so you can resume later.

## Ending a Game

Nothing fancy exit at any time with `ctrl+c` or wait until all the tracks have played and the game
will stop itself.
