from datetime import datetime
from random import randrange

from PIL import Image, ImageDraw, ImageFont


class User:
    def __init__(self):
        self.displayname = ""
        self.username = ""
        self.verified = False


class Tweet:
    def __init__(self):
        self.user = None
        self.content = ""
        self.time = None
        self.retweets = 0
        self.likes = 0
        self.replies = 0

    def render(self):
        img = Image.new("RGB", (590, 236), color="white")

        # Add avatar
        avatar = Image.open("res/img/trump.jpg").resize((48, 48))
        img.paste(avatar, (10, 10))

        cursor = ImageDraw.Draw(img)

        # Draw username
        displayname_font = ImageFont.truetype("res/font/Roboto-Black.ttf", 15)
        cursor.text(
            (70, 15), self.user.displayname, font=displayname_font, fill="#14171a"
        )
        username_font = ImageFont.truetype("res/font/Roboto-Regular.ttf", 12)
        cursor.text((70, 38), self.user.username, font=username_font, fill="#657786")

        # Draw message
        content_font = ImageFont.truetype("res/font/Roboto-Regular.ttf", 22)
        cursor.text((10, 70), self.content, font=content_font, fill="#14171a")

        # Draw timestamp
        date_font = ImageFont.truetype("res/font/Roboto-Regular.ttf", 12)
        cursor.text(
            (10, 110),
            self.time.strftime("%I:%M %p - %d %b %Y").lstrip("0"),
            font=date_font,
            fill="#657786",
        )

        # Draw stats
        highlight_stat_font = ImageFont.truetype("res/font/Roboto-Black.ttf", 13)
        cursor.text(
            (10, 157),
            "{:,}".format(self.retweets),
            font=highlight_stat_font,
            fill="#14171a",
        )
        stat_name_font = ImageFont.truetype("res/font/Roboto-Regular.ttf", 13)
        cursor.text((47, 157), "Retweets", font=stat_name_font, fill="#657786")
        cursor.text(
            (110, 157),
            "{:,}".format(self.likes),
            font=highlight_stat_font,
            fill="#14171a",
        )
        cursor.text((148, 157), "Likes", font=stat_name_font, fill="#657786")

        # Draw layout
        cursor.line((12, 145) + (578, 145), fill="lightgray")
        cursor.line((190, 145) + (190, 185), fill="lightgray")
        cursor.line((12, 185) + (578, 185), fill="lightgray")

        # Add verification
        if user.verified:
            verified = Image.open("res/img/verified.png").resize((15, 15))
            img.paste(verified, (187, 15), mask=verified)

        img.show()
        height = {1: 236, 3: 288}


if __name__ == "__main__":
    user = User()
    user.displayname = "Donald J. Trump"
    user.username = "@realDonaldTrump"
    user.verified = True

    tweet = Tweet()
    tweet.user = user
    tweet.content = "Spent too much time making a fake tweet maker.  Sad!"
    tweet.time = datetime.now()
    tweet.retweets = randrange(1000, 5000)
    tweet.likes = randrange(2 * tweet.retweets, 3 * tweet.retweets)
    tweet.replies = randrange(tweet.retweets)

    tweet.render()
