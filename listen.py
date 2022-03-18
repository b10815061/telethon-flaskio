from telethon import events
import asyncio
#from router import socketio

def listen(client):
    @client.on(events.NewMessage())
    async def event_handelr(evt):
        channel = await evt.get_chat()
        print(channel)
        print(channel.id)
        
        msgs =(await client.get_messages(channel.id,limit=5))
        
        for msg in msgs:
            print(msg.message)
        
        
        if(evt.raw_text=="disconnect"):
            print("goodbye")
            await client.disconnect()
        print(evt.raw_text)
        #socketio.emit('rcv_telegram_message',evt.raw_text)
        await asyncio.sleep(2)
        ### delete the input message
        await client.delete_messages(evt.chat_id,[evt.id])