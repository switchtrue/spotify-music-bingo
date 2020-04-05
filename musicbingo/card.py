from slugify import slugify
from PIL import Image, ImageDraw, ImageFont


class MusicBingoCard:
    def __init__(self, playlist, id_):
        self.id_ = id_
        self.playlist = playlist
        self.tracks = playlist.get_card_tracks()

    def get_filename(self):
        name = slugify(self.playlist.name())
        num = str(self.id_).zfill(3)
        return '{}_{}.png'.format(name, num)

    def write(self):
        WIDTH = 1000
        HEIGHT = 1200

        BINGO_TITLE_Y = 30
        PLAYLIST_TITLE_Y = 20

        CELL_WIDTH = 160
        CELL_HEIGHT = CELL_WIDTH
        CELL_PADDING = 5
        BOARD_X = 100
        BOARD_Y = 130

        img = Image.new('RGB', (WIDTH, HEIGHT), color=(240, 240, 240))
        d = ImageDraw.Draw(img)

        # BINGO Title
        fnt = ImageFont.truetype('Arial Unicode.ttf', 100)
        bingo_title_size = d.textsize("B   I   N   G   O", font=fnt)
        bingo_title_x = (WIDTH / 2) - (bingo_title_size[0] / 2)
        d.text((bingo_title_x, BINGO_TITLE_Y), "B   I   N   G   O", font=fnt, fill=(0, 0, 0))

        # Playlist Title
        fnt = ImageFont.truetype('Arial Unicode.ttf', 40)
        playlist_title_size = d.textsize(self.playlist.name(), font=fnt)
        playlist_title_x = (WIDTH / 2) - (playlist_title_size[0] / 2)
        playlist_title_y = BINGO_TITLE_Y + PLAYLIST_TITLE_Y + bingo_title_size[1]
        d.text((playlist_title_x, playlist_title_y), self.playlist.name(), font=fnt, fill=(0, 0, 0))

        # Add each of the bingo squares
        cells = self.tracks
        cells.insert(12, None)
        y1 = BOARD_Y
        fnt = ImageFont.truetype('Arial Unicode.ttf', 20)
        for idx, track in enumerate(cells):
            x1 = BOARD_X + ((idx % 5)*CELL_WIDTH)
            if idx % 5 == 0:
                y1 = y1 + CELL_HEIGHT

            x2 = x1 + CELL_WIDTH
            y2 = y1 + CELL_HEIGHT

            d.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255), outline=(0, 0, 0))

            if track:
                title = '{} - {}'.format(track['name'], track['artists'])
                wrapper = TextWrapper(title, fnt, CELL_WIDTH-(CELL_PADDING*2))
                wrapped_text = wrapper.wrapped_text()
                d.text((x1+CELL_PADDING, y1+CELL_PADDING), wrapped_text, font=fnt, fill=(0, 0, 0))
            else:
                free_space_fnt = ImageFont.truetype('Arial Unicode.ttf', 30)

                free_size = d.textsize('Free', font=free_space_fnt)
                space_size = d.textsize('Space', font=free_space_fnt)
                free_space_height = free_size[1] + space_size[1]

                free_x = x1 + (CELL_WIDTH / 2) - (free_size[0] / 2)
                free_y = y1 + (CELL_HEIGHT / 2) - free_size[1]
                d.text((free_x, free_y), 'Free', font=free_space_fnt, fill=(0, 0, 0))

                space_x = x1 + (CELL_WIDTH / 2) - (space_size[0] / 2)
                space_y = y1 + (CELL_HEIGHT / 2)
                d.text((space_x, space_y), 'Space', font=free_space_fnt, fill=(0, 0, 0))

        # Add a watermark footer link
        fnt = ImageFont.truetype('Arial Unicode.ttf', 16)
        footer_y = BOARD_Y + (CELL_HEIGHT*6) + 5
        d.text((560, footer_y), 'https://github.com/switchtrue/spotify-music-bingo', font=fnt, fill=(100, 100, 100))

        img.save(self.get_filename())


# From: https://stackoverflow.com/a/49719319/990416
class TextWrapper(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l
        ]
        self.font = font
        self.max_width = max_width

        self.draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(100, 100)
            )
        )

        self.space_width = self.draw.textsize(
            text=' ',
            font=self.font
        )[0]

    def get_text_width(self, text):
        return self.draw.textsize(
            text=text,
            font=self.font
        )[0]

    def wrapped_text(self):
        wrapped_lines = []
        buf = []
        buf_width = 0

        for line in self.text_lines:
            for word in line.split(' '):
                word_width = self.get_text_width(word)

                expected_width = word_width if not buf else \
                    buf_width + self.space_width + word_width

                if expected_width <= self.max_width:
                    # word fits in line
                    buf_width = expected_width
                    buf.append(word)
                else:
                    # word doesn't fit in line
                    wrapped_lines.append(' '.join(buf))
                    buf = [word]
                    buf_width = word_width

            if buf:
                wrapped_lines.append(' '.join(buf))
                buf = []
                buf_width = 0

        return '\n'.join(wrapped_lines)
