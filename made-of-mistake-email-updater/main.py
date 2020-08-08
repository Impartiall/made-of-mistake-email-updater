#!../venv/bin/python3

# made-of-mistake-email-updater - It does exactly what it says on the tin.
# Copyright (C) 2020  Jesse Looney

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from lxml import html

import toml

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from pathlib import PurePath, Path


def main() -> None:
    """
    Read configuration from TOML file, check for new comics, and send updates accordingly.
    """

    config: dict = toml.load(PurePath(
        Path.home(),
        ".config/made-of-mistake-email-updater.toml",
    ))

    previous_comic_name_file_path = PurePath(
        Path(__file__).parent.absolute(),
        ".previous_comic_name.txt",
    )

    previous_comic_name: str = get_previous_comic_name(previous_comic_name_file_path)
    current_comic_name: str = get_current_comic_name()

    if previous_comic_name != current_comic_name:
        set_previous_comic_name(
            current_comic_name,
            previous_comic_name_file_path,
        )

        print("Sending emails")
        send_emails(current_comic_name)
    else:
        print("No new comic found")


def get_previous_comic_name(path: PurePath) -> str:
    """
    Return the latest known comic name from a file.
    """
    with open(path, "r") as f:
        return f.readline().strip("\n")


def set_previous_comic_name(name: str, path: PurePath) -> None:
    """
    Write a comic name to a file.
    """
    with open(path, "w") as f:
        f.write(name)


def get_current_comic_name() -> str:
    """
    Return the newest Made of Mistake comic title.
    """
    url = "https://madeofmistake.com"
    response = requests.get(url)

    if not response.status_code == 200:
        raise Exception(f"An error occurred while making a request to '{url}': {response.status_code}")
    else:
        page = html.fromstring(response.content)
        return page.xpath("/html/head/title/text()")[0]


def send_emails(comic_title: str) -> None:
    pass


if __name__ == "__main__":
    main()
