<div align='center'>
<picture>
    <img width=250 alt="pychord-bot-logo" src="img/logo.png"/>
</picture>
</div>

<hr>

A telegram bot that exploits the power of [pychord](https://pypi.org/project/pychord/) library to:

 - Analyse a chord, given its name (e.g. `Cm7`)
 - Compose a chord, given its notes (e.g. `A C# E`)

## How to use
You can find the bot at [@pychordBot](https://t.me/pychordBot).

Send it the `/help` command to get the list of available commands, and you will be answered with the instructions for each one.

Currently the bot supports the following commands:

 - `/help` - Show the list of available commands
 - `/chord` - Analyse a chord (sent with the format `[Cm7]`)
 - `/compose` - Compose a chord (sent with the format `{A C# E}`)

The bot can be used also with the [inline mode](https://core.telegram.org/bots/inline), by typing `@pychordBot` in any chat and then requesting an analysis or a composition with the same format as above.

<hr>

## How to run
First of all you need to set (as _environment variable_) the `BOT_TOKEN` of your bot. You can get it from [@BotFather](https://t.me/BotFather).

Then you can run the bot with:
```bash
python3 main.py
```

Or you can set another _environment variable_ `WEBHOOK_URL` to enable the webhook mode. In this case, I recommend [`render`](https://render.com/)) as deployment and hosting platform.

N.B. Click [this link](https://render.com/deploy?repo=https://github.com/jacopo-massa/pychord-bot) or use the button below to automatically deploy (in a CI/CD fashion) this repository on render.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/jacopo-massa/pychord-bot)

<hr>

## GUNICORN CONFIGURATION
To host the bot on the major platforms, we need to use an HTTP server. I used [gunicorn](https://gunicorn.org/) with the `gevent` worker class. To work properly, gunicorn should be launched with the following command (that is be also the start command on `render`):
```bash
gunicorn -b 0.0.0.0:5000 main:app -k gevent -c geventlet-config.py
```
