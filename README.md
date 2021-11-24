# tgtg_bot

Too good to go bot to notify new baskets available via Discord using Heroku servers.

## How to init ?

Add your tokens (discord & tgtg) in `.env` and in Heroku and then link your repo to Heroku servers.

## How to use ?

For exemple with TicTic store with 48.3858100,-4.4893840 (GPS)

In the discord channel:
- Connect yourself with `connexion`
- The bot is On by default but you can turn it off with `off` then On with `on`
- Get your favorite store with `favorite` (it's turn off the bot)
- Add a favorite store with `add 48.3858100,-4.4893840`
- Remove a favorite store with `remove 48.3858100,-4.4893840`
- Focus the store you like with `focus favorite_id` or unfocus with `unfocus favorite_id`
- Get all the focus `get focus`
- Clear focus with `clear focus`

The bot will send you a notification when a basket is free in your favorites stores.

## Output

Favorite

![alt text](https://github.com/ThomasCochou/TooGoodToGo_Discord_Bot/blob/main/exemple%20favorite.png?raw=true)

Focus

![alt text](https://github.com/ThomasCochou/TooGoodToGo_Discord_Bot/blob/main/exemple%20focus.png?raw=true)

Available

![alt text](https://github.com/ThomasCochou/TooGoodToGo_Discord_Bot/blob/main/exemple%20basket.png?raw=true)
