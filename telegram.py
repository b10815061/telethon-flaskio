from telethon import TelegramClient,events,functions
import asyncio
import dbconfig,psycopg2,listen,get_dialog
import get_message
from telethon.tl.functions.users import GetFullUserRequest

api_id = 12655046
api_hash = 'd84ab8008abfb3ec244630d2a6778fc6'


async def main():
    
    phone = input("phone:")
    
    client = TelegramClient(phone,api_id,api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        me = await client.sign_in(phone,input("mycode: "))
        print((await client.get_me()).stringify())    
    return
        
    #await client.send_message('testing','hello , myself!!')
    #print(await client.download_profile_photo('Telegram'))
    
    ### get all the friends(channels) and the content of it  
    await get_dialog.get(client)
    
    #await get_message.get_channel_message(client,'testing')
    
    ### listening on the message , print out the sender channel
    listen.listen(client)
    
    
    
    ### always running
    await client.run_until_disconnected()
    
asyncio.run(main())
        
