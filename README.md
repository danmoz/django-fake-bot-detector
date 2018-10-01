# django-fake-bot-detector 

Detect and block fake search bots 🤖

## Overview

Many nefarious internet bots, knowing they are not welcome, like to fake their user-agent
string so they can pretend they're just a friendly search bot (e.g. GoogleBot) hitting your site.

Fortunately the major search bots are all verifiable by performing a reverse DNS lookup against
the request IP and checking the returned domain matches the expected domain 
(e.g. `crawl-66-249-66-1.googlebot.com`). This simple middleware for Django does exactly that.

## Installation

Add the middleware:

```
MIDDLEWARE = [
    ...
    'fakebotdetector.middleware.FakeBotDetectorMiddleware',
    ...
]
```

## Settings

You can use the following in your settings.py

| Name                            | Description                                                      | Default |
|---------------------------------|------------------------------------------------------------------|---------|
| FAKE_BOT_DETECTOR_ENABLED       | Enables the fake bot detector                                    | True    |
| FAKE_BOT_RESPONSE_CODE          | The HTTP status code to send for blocked requests                | 403     |

*Pro tip:* if you are running django behind an NGINX proxy, you can set FAKE_BOT_RESPONSE_CODE to 444 to have
NGINX close the connection immediately without sending an HTTP response at all.

## Django Signals

A `fake_bot_hit` signal is sent every time the middleware blocks a bot.

To listen for the signal, simply set up a receiver:

```
from django.dispatch import receiver
from fakebotdetector.signals import fake_bot_hit

@receiver(fake_bot_hit)
def fake_bot_hit_receiver(sender, bot_ip, bot_useragent, fqdn_expected, fqdn_received, **kwargs):
    print('Received a fake bot hit from {}'.format(bot_ip))
```