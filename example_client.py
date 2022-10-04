from src import bot
from os import environ as env

FourmsBot = bot("ShowierData9978", env["sec"] )
FourmsBot.current_parsing = 1

async def pre_message(message, bot=FourmsBot):
  bot.current_parsing += 1
  print(f"{message['username']}: {message['raw']}")
  
  
  if len(bot.loop.last_gotten_posts) == bot.current_parsing:
      await bot.api.send_post(input(">"), message['topic_id'])
      bot.current_parsing = 1
  
  
FourmsBot.callback(pre_message, "raw_pre_post")

FourmsBot.run()