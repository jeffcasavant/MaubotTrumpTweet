# MaubotTrumpTweet

A plugin for Maubot that generates tweets from Trump.

Usage:

```
!trump Spent too long making a fake tweet generator.  Sad!
```

# Installation

On your Maubot system, install wkhtmltopdf.  Download `.mbp` from the latest
release.  Upload to your Maubot installation and connect it to an instance as
normal.

# Building

`make build`

This requires `poetry-plugin-export`, which is a Poetry plugin that has to be installed separately.  Install it with [`pip` or `pipx inject`](https://python-poetry.org/docs/plugins/#using-plugins)^.

# Future improvements
* Factor out the tweet generation fully into a separate library
* Set the user up to add additional tweet users
* Add more avatars - be mindful of licensing
* Expand layouting to allow stats <1000 and >9999
* Fine-tune image alignment

# Notes
* This is not great python code
* Real avatars from https://uifaces.co/
* Cartoons from https://avachara.com/avatar/gallery.php
