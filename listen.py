from telethon import events
import asyncio
from flask_socketio import emit

def listen(client,socketio):
    @client.on(events.NewMessage())
    async def event_handelr(evt):
        channel = await evt.get_chat()
        #print("listening")
        '''print(channel)
        print(channel.id)'''
        
        msgs =(await client.get_messages(channel.id,limit=1))
        
        for msg in msgs:
            print(msg.message)
        
        socketio.emit('my_response',{'data':msg.message,'count':channel.id})
        
        
        if(evt.raw_text=="disconnect"):
            print("goodbye")
            await client.disconnect()