# made-of-mistake-email-updater
A Python script for sending email updates when a new [Made of Mistake](https://madeofmistake.com) comic has been posted, written in the FP style.

# Installation
Follow these steps if you would like to use this program for yourself.

*DISCLAIMER: Although this program should work on most systems, it has only been tested on Ubuntu 18.04.3 LTS.*

## Get the code
Clone the repository into the directory of your choice.
```
git clone https://github.com/Impartiall/made-of-mistake-email-updater.git
```

## Install dependencies
This program runs on [Python 3](https://python.org) (tested on v3.6.9), so install that using the package manager of your choice.

If you would like to manage dependencies with an virtual environment, note that the script shebang looks in the parent of its directory for a virtual environment called `venv/` by default.

Run the following command to install all dependencies with [pip](https://pypi.org/project/pip/):
```
pip install requests lxml toml
```

## Create a gmail account
Create a Gmail account which will be responsible for sending email notifications. **Do *not* use your regular Gmail account for this step and do not use this secondary account for any logins.** For ease of use, this program does not authenticate with [OAuth 2.0](https://www.oauth.com/) [like Google recommends](https://developers.google.com/identity/protocols/oauth2), but instead uses an [app password](https://support.google.com/accounts/answer/185833). This is fairly secure, but do not rely on it for something as important as a personal email.

Follow [this link](https://support.google.com/accounts/answer/185833) to set up 2 Factor Authentication and generate an app password. Copy the app password for the next step.

## Configure settings
Create a file `.config.toml` (note the dot before 'config') in the same directory as `made-of-mistake-email-updater/main.py` and open it in your preferred editor.

Add the following settings:
```
receivers = [
  "example@gmail.com",
  "example@yahoo.com",
  ...
]

[sender_login]
  email = "myemailbot@gmail.com",
  password = "<app-password>"
```

Paste the app password from the last step into the sender_login.password field.
Emails will be sent to each of the emails in the receivers list when a new comic is detected.

# Run it on an interval
On linux, consider using [cron](https://www.man7.org/linux/man-pages/man8/cron.8.html) to run this program on an interval.

Simply link the `main.py` file into one of `/etc/cron.{hourly|daily|weekly|monthly}`:
```
ln -s path/to/main.py /etc/cron.daily/made-of-mistake-email-updater
```
