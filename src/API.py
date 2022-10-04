import os
import asyncio

import aiohttp
from aiohttp import ClientConnectionError
from loop import LoopMngr


from urllib.parse import urljoin
import json

import datetime

class API:
  def __init__(self, loop:LoopMngr, token, username):
    self.loop = loop
    self.session = None
    self.base_url = loop.server_url
    self._token = token
    self._username = username

  async def async_init(self):
    self.session = aiohttp.ClientSession(loop=self.loop.asyncio_loop, headers={
      'Api-Key':self._token, "Api-Username":self._username
    })
  
  async def send_post(self, msg, where, extra_data=None):
    try:
      data= {
        "raw": msg,
        "category": where,
        "created_at": str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
      }
      if extra_data is not None:
        data.update(extra_data)

      async with self.session.post(urljoin(self.base_url, "/posts.json"), data=json.dumps(data)) as resp:
        if resp.status == 200:
          return await resp.json()
        else:
          print(await resp.text())
          return None
                  
    except asyncio.TimeoutError:
      pass #ignore 

    except ClientConnectionError:
      pass #ignoreing 

    except Exception as e:
       print(f'Error: {e.__class__.__name__}: {e}') 


  async def create_topic(self, title, post, category=None, extra_data=None):
      data= {
        "title": title,
        "category": category,
      }
      if category is None:
        del data[ "category" ]
      if extra_data is not None:
        data.update(extra_data)

      return await self.send_post(post, 0, data)

  async def send_private(self, msg, users, extra_data=None):
    data= {
      "target_recipients":",".join(users)
    }
    if extra_data is not None:
      data.update(extra_data)

    return await self.send_post(msg, 0, data)

  async def create_private(self, msg, users, extra_data=None):
    data= {
      "archetype": "private"
    }
    
    if extra_data is not None:
      data.update(extra_data)
    
    return await self.send_private(msg, users, data)

if __name__ == "__main__":

  async def main():
    loop = asyncio.get_event_loop()
    my_secret = os.environ['sec']
    async def handle_post(post):
      print(f"{post['username']}: {post['raw']}")
      if lp.state == 0:
        print(await lp.api.create_topic(post['username'], post['raw'], 2))
        lp.state = 1
    lp = LoopMngr("https://forums.meower.org/", handle_post, loop)
    api = API(lp, my_secret, "ShowierData9978")
    lp.api = api
    lp.state = 0 
    await api.async_init()
    await lp.start()
  
  asyncio.run(main())