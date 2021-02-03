# Inworks Twitter Bot

This repo contains the Python source code for the Inworks Twitter Bot, known affectionately as [**Inworks Joe**](https://twitter.com/Inworks_Joe). Joe is designed to output selected data from  [**MakerOS' API**](https://inworks.makeros.com) into [**Twitter's API**](https://developer.twitter.com/en/docs) to give insight into the featured prototyping and design projects Inworks staff is working on.

## Current Functionality

These are the current stable features of Joe (`twitter_bot.py`).

#### TWEET CHANGE
- The bot currently works by pulling the "featured" project description and comparing it to a stored string.
- If the strings do not match this means there is a change in the description and we post it as a status.
- The goal is to make this change based on "progress" instead of description changes

#### AUTO REPLY
- The auto reply feature works currently if someone Tweets regularly while mentioning @Inworks_Joe along with a few keywords.
- Keywords: Hey, hi, hello, joe, yo, sup, whats, support, help. I believe the goal will be to make it reply on any mention period. **Note: has bugs**
- at the moment the bot sometimes does not reply in a comment but as a status change(Tweet).


## Skill-building
This code utilizes a couple of novel concepts that are useful in a programmer's toolkit, namely:
- Using one service's API for data output into another service's API for data input.
- Using the json library to easily parse data into objects.
- Practical application of using a dictionary data structure.
- Industry standard practice for hiding sensitive data (e.g. API keys).

## Getting Started
**NOTE: This README assumes the user is using a Unix-based Terminal to issue commands to the operating system.**
1. Check that git is installed on your machine with `git --version`.
2. Clone this repository onto your computer with `git clone https://github.com/Inworks/twitter-bot.git`
3. Check that Python 3 is installed with `python3 --version`.

If an error message is returned as a result of those commands, then please Google how to install git or Python 3 on your computer.

## Dependencies
This project needs a couple of dependencies in order to run.
It requires **Python 3**, the Python package manager **pip** and the Python virtual environment **venv**. Documentation for installing and configuring pip and env can be [**found here**](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

After dependencies are installed, run this command in the working directory of your bot:
```
$ python3 -m venv python-env
$ source ./python-env/bin/activate
$ python3 -m pip install --upgrade pip # this ensures you're using the updated version of pip
$ pip install tweepy requests
```

The steps above are required in order to avoid installing Python packages on our entire machine (i.e. they are installed in project directory only).

## Configuration

Credentials and tokens for your own MakerOS API and Twitter API instances need to be added to the `init-credentials.sh` script and executed in your working directory by using the Terminal command `source ./init-credentials.sh`. **If you plan to work in a public GitHub repo please note that you should rename this file and add its revised name to the .gitignore file.** These credentials are stored as environment variables in the OS and then accessed by the `twitter_config.py` and `makeros_functions.py` files. For more information about Twitter's access token architecture **[click here](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens)**.


### For Inworks Employees

Our script for setting environment variables can be accessed on the Inworks file server in the `/Space/Downtown Lab/APIs`.
