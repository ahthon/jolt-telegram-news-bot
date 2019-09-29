# Jolt, a Telegram news bot

![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)

We want news readers to start discussions about news they care about and feel empowered by it.

Contents:

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Future optimisations](#future-optimisations)
6. [Acknowledgements](#acknowledgements)
7. [Team](#team)

# 1. Introduction

[Prototype] Jolt is a Telegram bot for users to read Singapore news and to create their own personal news bulletins.

# 2. Requirements

* newsapi-python == 0.2.5
* newspaper3k == 0.2.5
* python-telegram-bot == 12.1.1

# 3. Setup

1. Create a bot with Telegram's [Bot Father](https://telegram.me/botfather) bot. A guide to creating a bot with Bot Father can be found [here](<https://core.telegram.org/bots#6-botfather>).
2. Pass in your bot's API token in `main.py`:
```python
TOKEN = 'token'  # insert your telegram bot token here
```
3. Create an account with [newsapi.org](https://newsapi.org/) to get your newsapi key.

4. Pass in your key for newsapi in `newsfeed.py`:
```python
KEY = 'key'  # insert your newsapi key here
```
5. The bot is now ready. Run `main.py` to run the bot.

# 4. Usage

### Demo

<img src="https://github.com/ahthon/jolt-telegram-news-bot/blob/master/jolt_demo.gif" alt="Jolt demo" height="450" align="center">

### Commands
Jolt uses slash commands to execute tasks.

* `/start` sends the news bulletin.
* `/search` initiates a news search. Use `/search <your search query>` to immediately get Jolt to search for `<your search query>`.
* `/help` shows the user what Jolt can do.

### News bulletin menus

Jolt uses [inline keyboards](https://core.telegram.org/bots/2-0-intro#new-inline-keyboards) to build its menus.

#### Main menu
The main menu presents the user with a list of five of the top headlines for Singapore news from newsapi.org.

#### Sub-menu
Clicking to read the story from the bulletin's main menu shows the individual news stories that have been summarised using newspaper3k. 

Users may also:

* read the full story by clicking the `Read full story here` hyperlink;
* toggle to other stories of the same topic using the story's navigation buttons, `Prev` or `Next`;
* or return to the main menu with the `Return to stories` button.

# 5. Future optimisations

What we have now is a working prototype. We hope to improve and add on to Jolt's current capabilities. These include:

* A user interface for news personalisation and scheduling.
* Having a better user experience (UX), such as smoother tutorials for first-time users.
* Being able to handle conversations in a casual or more organic manner.
* Being able to subsrcribe to specific news tags or keywords.
* Being able 'like' news stories to gauge its popularity.
* Having interactive quizzes.
* Enabling different types of content such as videos and podcasts to be easily accessible.

# 6. Acknowledgements

We would like to thank our news partners at The Straits Times, Sandra Davie and Azhar Kasman, and our mentor at Google, Kate Beddoe, for their expert guidance. We would also like to extend our thanks to our first prototype users, Lin Shan, Gracia, and Melissa, for their invaluable feedback. Lastly, we want to thank our instructors Jessica Tan and Joan Kelly for their continuous support and encouragement during our design thinking process.

# 7. Team

Anthony ([ahthon](https://github.com/ahthon)), Christy, Iskandar, Kenneth, Michael, and Theophilus.
