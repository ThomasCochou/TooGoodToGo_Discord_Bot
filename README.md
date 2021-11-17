# tgtg_bot

Too good to go bot to notify via Discord when a basket is free using Heroku servers.

## How to init ?

Add your tokens (discord & tgtg) in `.env` and in Heroku and then link your repo to Heroku servers.

## How to use ?

For exemple with TicTic store with 48.3858100,-4.4893840 (GPS)

In the discord channel:
- Connect yourself with `connexion`
- Add a favorite store with `add:48.3858100,-4.4893840`
- Remove a favorite store with `remove:48.3858100,-4.4893840`
- Get your favorite store with `get stores`

The bot will send you a notification when a basket is free in your favorites stores.

## Output

![alt text](https://github.com/ThomasCochou/TooGoodToGo_Discord_Bot/blob/main/exemple%20screen.png?raw=true)
