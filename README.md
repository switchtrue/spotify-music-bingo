# Spotify Music Bingo

Generate bing cards from a Spotify playlist and then play short clips of each song to play music
bingo.

Check out the [sample](samples) Bingo cards.

# Installation

1. Clone this repository
2. pip install -r requirements.txt

# Prerequisites

1. You'll need a Spotify Premium account.
2. You need to create a Spotify application [here](https://developer.spotify.com/dashboard/applications)
and obtain its `Client ID` and `Client Secret`.

# Usage

## Generate Bingo Cards

`scripts/bingo.sh generate-cards --playlist <playlist_url> --cards 5`

See below for the playlist URL required.

## Start a New Game

`scripts/bingo.sh play-game --playlist <playlist_url> [--clip-duration <seconds>] [--duration-between-clips <seconds>] [--verbose]`

`--clip-duration` is optional and controls how much of the beginning of the track is played. The
default is 30 seconds.

`--duration-between-clips` is optional and allows a silent gap to be played between each clip to
better identify the start/end of a song. The default is 2 seconds.

`--verbose` will log each track after it has played.

## Resuming a Game

The order of the tracks played is randomised when a game is started. However, you can pass in a
`game id` that get used to seed the randomisation of the tracks. When a new game is started the
game id is displayed and can be passed back in with a starting track number to carry on where you
left off.

`scripts/bingo.sh play-game --playlist <playlist_url> --game-id <game_id> --starting-track <track_number> [--clip-duration <seconds>] [--duration-between-clips <seconds>]`

When you exit a game the `--game-id` and `--starting-track` will be output so you can resume later.

## Ending a Game

Nothing fancy exit at any time with `ctrl+c` or wait until all the tracks have played and the game
will stop itself.

# Notes

## Playlist URLs

Playlist URLs should be in the format of a share link like the following:
`https://open.spotify.com/playlist/37i9dQZF1DX2S9rTKTX6JP?si=dNmprcd1Qt6DePO606aOHA`

You can obtain these by clicking "Share" > "Copy Playlist Link" on a Spotify playlist.

## Playing via Zoom

The concept for this orginated during the COVID-19 pandemic when social distancing was key. As such
people were encouraged to stay at home and public spaces were closed meaning music bingo couldn't be
played at the local pub.

Instead I sought to find a way to play it via video conference and therefore it only seems right to
include instructions for playing via [Zoom](https://zoom.us/).

On the host computer, sign in to Zoom, start a meeting, Click "Share Screen" at the bottom and then
select the "Advanced" tab and choose the "Music or Computer Sound Only" option. All other participants
need to join the Zoom meeting as per any other Zoom meeting.
