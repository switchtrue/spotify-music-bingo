# Spotify Music Bingo

Generate bing cards from a Spotify playlist and then play short clips of each song to play music
bingo.

# Installation

1. Clone this repository
2. pip install -r requirements.txt

# Usage

## API Tokens

When using the commands in this project you need to provide Spotify developer credentials in the
form of a client id and client secret.
These must be set as the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables.

## Generate Bingo Cards

`SPOTIPY_CLIENT_ID=... SPOTIPY_CLIENT_SECRET=... scripts/bingo.sh generate-cards --playlist <playlist_url> --cards 5`
