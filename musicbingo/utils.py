from .constants import DEFAULT_TRACK_COUNT

def generate_play_game_command(playlist_url, game_id, track_count, starting_track=None):
    cmd = "\tscripts/bingo.sh play-game --playlist=\"{}\" --game-id={}".format(playlist_url, game_id)

    if track_count != DEFAULT_TRACK_COUNT:
        cmd = "{} --track-count={}".format(cmd, track_count)

    if starting_track is not None:
        cmd = "{} --starting-track={}".format(cmd, starting_track)

    return cmd
