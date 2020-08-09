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

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl

from pathlib import PurePath, Path


def main() -> None:
    """
    Read configuration from TOML file, check for new comics, and send updates accordingly.
    """

    config: dict = toml.load(PurePath(
        Path(__file__).parent.absolute(),
        ".config.toml",
    ))

    previous_comic_name_file_path = Path(
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

        send_emails(config["sender_login"], config["receivers"], current_comic_name)
    else:
        print("No new comic found")


def get_previous_comic_name(previous_comic_name_file_path: Path) -> str:
    """
    Read the latest known comic name from a file.

    Args:
      previous_comic_name_file_path: File path to the file that stores the previous comic name.
    
    Returns:
      The latest known comic name.
    """
    if not previous_comic_name_file_path.exists():
        previous_comic_name_file_path.open("x")

    with previous_comic_name_file_path.open() as f:
        return f.readline().strip("\n")


def set_previous_comic_name(name: str, previous_comic_name_file_path: Path) -> None:
    """
    Write a comic name to a file.

    Args:
      name: The new name to store in the previous_comic_name_file.
      previous_comic_name_file_path: File path to the file that stores the previous comic name.
    """
    with previous_comic_name_file_path.open("w") as f:
        f.write(name)


def get_current_comic_name() -> str:
    """
    Get the newest Made of Mistake comic title from the webpage.

    Returns:
      The newest comic name.

    Raises:
      Exception: If the request does not get a 200 OK response.
    """
    url = "https://madeofmistake.com"
    response = requests.get(url)

    if not response.status_code == 200:
        raise Exception(f"An error occurred while making a request to '{url}': {response.status_code}")
    else:
        page = html.fromstring(response.content)
        return page.xpath("/html/head/title/text()")[0]


def send_emails(sender_login: dict, receivers: list, comic_title: str) -> None:
    """
    Send an email message to each configured receiver.
    
    Args:
      sender_login: Dictionary containing the email and password of the sender.
      receiver: List of email addresses of receivers.
      comic_title: Title of the comic the email message is about.
    """
    print(f"Sending emails as: '{sender_login['email']}'")

    subject = f"{comic_title} - A new Made of Mistake comic"
    message_text = (
        f"Made of Mistake just released a new comic: {comic_title}\n\n"
        "View it at www.madeofmistake.com"
    )
    message_html = (
        f"Made of Mistake just released a new comic: <a href='https://madeofmistake.com'>{comic_title}</a>"        
    )

    messages = [
        create_message(
            sender_login["email"],
            receiver,
            subject,
            message_text,
            message_html
        ) for receiver in receivers
    ]

    [
        send_message(sender_login, receiver, message)
        for receiver, message in zip(receivers, messages)
    ]

    print("Done")


def send_message(sender_login: dict, receiver: str, message: str) -> None:
    """
    Send an email message.

    Args:
      sender_login: Dictionary containing the email and password of the sender.
      recevier: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The body text of the email message.
    """
    print(f"  Emailing '{receiver}'")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender_login["email"], sender_login["password"])
        server.sendmail(sender_login["email"], receiver, message)


def create_message(sender: str, receiver: str, subject: str, message_text: str, message_html: str) -> str:
    """
    Create a message for an email.

    Args:
      sender: Email address of the sender.
      receiver: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The body text used in plain rendering of the email message.
      message_html: The body html used in html rendering of the email message.

    Returns:
      A MIMEMultipart email message with plain and html rendering options.
    """
    message = MIMEMultipart("alternative")
    message["to"] = receiver
    message["from"] = sender
    message["subject"] = subject

    message.attach(MIMEText(message_text, "plain"))
    message.attach(MIMEText(message_html, "html"))

    return message.as_string()


if __name__ == "__main__":
    main()
