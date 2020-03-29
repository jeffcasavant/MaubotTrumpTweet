from datetime import datetime
from io import BytesIO
from os import listdir, path
from random import randrange, choice
from textwrap import wrap
import sys
import zipfile

from PIL import Image, ImageDraw, ImageFont
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.client.api.types.event.message import MediaMessageEventContent, ImageInfo

BASE_PATH = path.dirname(path.realpath(__file__))


def list_avatars():

    avatar_path = "res/img/avatars"

    if BASE_PATH.endswith(".mbp"):
        mbp = zipfile.ZipFile(BASE_PATH)
        return [path.basename(file.filename) for file in mbp.infolist() if file.filename.startswith(avatar_path)]
    else:
        return listdir(avatar_path)


def load_resource(path: str):

    if BASE_PATH.endswith(".mbp"):
        mbp = zipfile.ZipFile(BASE_PATH)
        return mbp.open(path)
    else:
        return open(path, "rb")


def human_fmt(n):
    for mag, abbr in [(1000000, "M"), (1000, "K")]:
        if n > mag:
            return "{:.1f}{}".format(n / mag, abbr)
    return str(n)


class User:
    def __init__(self):
        self.avatar = ""
        self.displayname = ""
        self.username = ""
        self.verified = False


class Tweet:

    _width = 590
    _border = 10

    def __init__(self, user, content):
        self.user = user
        self.content = content
        self.time = datetime.now()
        self.retweets = randrange(1000, 5000)  # nosec
        self.likes = randrange(self.retweets, 2 * self.retweets)  # nosec
        self.replies = randrange(self.retweets)  # nosec

    @classmethod
    def _draw_message_multicolored(cls, img, content, content_font, height):
        text_color = "#14171a"
        link_color = "#0084b4"
        y_text = 70
        fill = " @ "

        tmp = Image.new("RGB", (2000, height), color="white")  # scrap image
        cursor = ImageDraw.Draw(tmp)
        w_fill, y = cursor.textsize(fill, font=content_font)

        for line in content:
            _, height = content_font.getsize(line)
            x_draw, x_paste = 0, cls._border
            current_color = text_color
            for char in line:
                if char in ["@", "#"]:
                    current_color = link_color
                elif current_color != text_color and not (char.isalpha() or char == "_"):
                    current_color = text_color
                w_full = cursor.textsize(fill + char, font=content_font)[0]
                w = w_full - w_fill
                cursor.text((x_draw, y_text), fill + char, font=content_font, fill=current_color)
                cut = tmp.crop((x_draw + w_fill, y_text + 1, x_draw + w_full, y_text + y))
                img.paste(cut, (x_paste, y_text))
                x_draw += w_full
                x_paste += w
            y_text += height

    def render(self):
        content = wrap(self.content, width=50)
        height_addl = 24 * (len(content) - 1)

        img = Image.new("RGB", (Tweet._width, 236 + height_addl), color="white")

        # Add avatar
        avatar = Image.open(load_resource(self.user.avatar)).resize((48, 48))
        avatar_mask = Image.new("L", (48, 48))
        mask_draw = ImageDraw.Draw(avatar_mask)
        mask_draw.ellipse((0, 0) + (48, 48), fill=255)
        img.paste(avatar, (Tweet._border, Tweet._border), mask=avatar_mask)

        cursor = ImageDraw.Draw(img)

        # Draw username
        displayname_font = ImageFont.truetype(load_resource("res/font/Roboto-Black.ttf"), 15)
        cursor.text((70, 15), self.user.displayname, font=displayname_font, fill="#14171a")
        username_font = ImageFont.truetype(load_resource("res/font/Roboto-Regular.ttf"), 12)
        cursor.text((70, 38), self.user.username, font=username_font, fill="#657786")

        # Draw message
        content_font = ImageFont.truetype(load_resource("res/font/Roboto-Regular.ttf"), 22)
        self._draw_message_multicolored(img, content, content_font, img.height)

        # Draw timestamp
        date_font = ImageFont.truetype(load_resource("res/font/Roboto-Regular.ttf"), 12)
        cursor.text(
            (Tweet._border, 115 + height_addl),
            self.time.strftime("%I:%M %p - %d %b %Y").lstrip("0"),
            font=date_font,
            fill="#657786",
        )

        # Draw stats
        highlight_stat_font = ImageFont.truetype(load_resource("res/font/Roboto-Black.ttf"), 13)
        cursor.text(
            (Tweet._border, 157 + height_addl), "{:,}".format(self.retweets), font=highlight_stat_font, fill="#14171a",
        )
        stat_name_font = ImageFont.truetype(load_resource("res/font/Roboto-Regular.ttf"), 13)
        cursor.text((47, 157 + height_addl), "Retweets", font=stat_name_font, fill="#657786")
        cursor.text(
            (110, 157 + height_addl), "{:,}".format(self.likes), font=highlight_stat_font, fill="#14171a",
        )
        cursor.text((148, 157 + height_addl), "Likes", font=stat_name_font, fill="#657786")

        # Draw layout
        line_start = Tweet._border + 2
        line_end = Tweet._width - line_start
        topline_height = 145 + height_addl
        bottomline_height = 185 + height_addl
        vertical_width = 190
        cursor.line((line_start, topline_height) + (line_end, topline_height), fill="lightgray")
        cursor.line(
            (vertical_width, topline_height) + (vertical_width, bottomline_height), fill="lightgray",
        )
        cursor.line(
            (line_start, bottomline_height) + (line_end, bottomline_height), fill="lightgray",
        )

        # Add side avatars
        avatar_base_width = vertical_width + 10
        avatars = list_avatars()
        small_avatar_mask = Image.new("L", (20, 20))
        mask_draw = ImageDraw.Draw(small_avatar_mask)
        mask_draw.ellipse((0, 0) + (20, 20), fill=255)
        for index in range(10):
            avatar = Image.open(load_resource("res/img/avatars/{}".format(choice(avatars)))).resize((20, 20))  # nosec
            img.paste(
                avatar, (avatar_base_width + index * 24, 157 + height_addl), mask=small_avatar_mask,
            )

        # Add verification
        if self.user.verified:
            verified = Image.open(load_resource("res/img/verified.png")).resize((15, 15))
            img.paste(verified, (187, 15), mask=verified)

        # Add bottom stats summary
        bottomstats_text_height = 202 + height_addl
        reply = Image.open(load_resource("res/img/reply.png")).resize((20, 20))
        img.paste(reply, (10, 198 + height_addl), mask=reply)
        bottom_stat_font = ImageFont.truetype(load_resource("res/font/Roboto-Black.ttf"), 12)
        cursor.text(
            (45, bottomstats_text_height), human_fmt(self.replies), font=bottom_stat_font, fill="#657786",
        )
        retweet = Image.open(load_resource("res/img/retweet.png")).resize((26, 16))
        img.paste(retweet, (85, 200 + height_addl), mask=retweet)
        cursor.text(
            (125, bottomstats_text_height), human_fmt(self.retweets), font=bottom_stat_font, fill="#657786",
        )
        like = Image.open(load_resource("res/img/like.png")).resize((20, 20))
        img.paste(like, (165, 200 + height_addl), mask=like)
        cursor.text(
            (200, bottomstats_text_height), human_fmt(self.likes), font=bottom_stat_font, fill="#657786",
        )

        return img


def trump_user():
    user = User()
    user.avatar = "res/img/trump.jpg"
    user.displayname = "Donald J. Trump"
    user.username = "@realDonaldTrump"
    user.verified = True

    return user


def render_tweet(message):
    trump = trump_user()
    tweet = Tweet(trump, message)

    file = BytesIO()
    img = tweet.render()
    img.save(file, format="png")
    return img


class TrumpTweetPlugin(Plugin):
    @command.new("trump")
    @command.argument("message", pass_raw=True, required=True)
    async def handler(self, evt: MessageEvent, message: str) -> None:
        await evt.mark_read()
        img = render_tweet(message)
        mxc_uri = await self.client.upload_media(file.getvalue(), mime_type="image/png")
        content = MediaMessageEventContent()
        info = ImageInfo()
        info.width, info.height = img.size
        info.mimetype = "image/png"
        content.info = info
        content.body = "tweet"
        content.msgtype = "m.image"
        content.url = mxc_uri

        await evt.respond(content)


if __name__ == "__main__":
    message = " ".join(sys.argv[1:])
    render_tweet(message).show()
