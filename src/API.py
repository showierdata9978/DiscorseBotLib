import asyncio

import aiohttp
from aiohttp import ClientConnectionError

from urllib.parse import urljoin
import json

import datetime

class API:
  def __init__(self, loop, token):
    self.loop = loop
    self.session = aiohttp.ClientSession(loop=loop.asyncio_loop, headers={'Authorization': 'Bearer'+ token})
    self.base_url = loop.server_url

  
  async def send_post(self, msg, where, extra_data=None):
    try:
      data= {
        "raw": msg,
        "topic_id": where,
        "category": 0,
        "created_at": str(datetime.datetime())
      }
      if extra_data is not None:
        data.update(extra_data)

      async with self.session.post(urljoin(self.base_url, "/posts.json"), data=data) as resp:
        if resp.status == 200:
          return resp.json()
        else:
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

  