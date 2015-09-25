# Small learning tool for helping GERMAN

It's focused on learning IT verbs and terms.

Steps:
* Create a Telegram bot account. Please check their website for further information.
* Install the Telegram client where you want to answer the germans questions (e.g PC, Android cell phone...)
* Go to your server and set the `BOT_TOKEN` environmental var with the TOKEN of your Telegram bot.
* Run the server: `python trainer.py verben.csv worter.csv`
* Enjoy and learn! The server will send you questions to your Telegram client.
* For switching between categories (verbs or words), just type `/verbs` or `/words` in the Telegram window.

## TODO:

* Better handling of multi clients
