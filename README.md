# Inworks Twitter Bot
![Inworks Bot aka Joe](./Inworksbot.png)
This repo contains the Python source code for the Inworks Twitter Bot. The Bot is designed to output selected data from our [**remote prototyping platform's API**](https://inworks.makeros.com) into [**Twitter's API**](https://developer.twitter.com/en/docs) to give insight into the featured prototyping and design projects Inworks staff is working on.

## Skill-building
This code utilizes a couple of novel concepts that are useful in a programmer's toolkit, namely:
- Using one service's API for data output into another service's API for data input.
- Using the json library to easily parse data into objects.
- Practical application of using a dictionary data structure.
- Industry standard practice for hiding sensitive data (e.g. API keys).

## Dependencies
This project needs a couple of dependencies in order to run.
It requires **Python 3** *(exact version number?)*, the Python package manager **pip** and the Python virtual environment **venv**. Documentation for installing and configuring pip and env can be [**found here**](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

After dependencies are installed, run this command in the working directory of your bot:
```
$python3 -m venv (name of vm)
$source ./(name of vm)/bin/activate
$pip install tweepy
```

The steps above are required in order to avoid installing the tweepy dependencies on our entire machine (i.e. they are installed in project directory only).

## Configuration

Below is how to configure the `config.py` file, which allows one to enter their personalized Twitter API tokens. For more information on these tokens [**click here**](https://developer.twitter.com/ja/docs/basics/authentication/guides/access-tokens).

Run the following in the working directory once you've enabled the vm *(virtual env?)* above. Enter your own keys found on your Twitter Dev portal instead of `(credentials)`.
```
$export CONSUMER_KEY="(credentials)"
$export CONSUMER_SECRET="(credentials)"
$export ACCESS_TOKEN="(credentials)"
$export ACCESS_TOKEN_SECRET="(credentials)"
```
