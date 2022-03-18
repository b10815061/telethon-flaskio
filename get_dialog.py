from sqlalchemy.orm import Session
from sqlalchemy import select
import model
from model import channels
from dbconfig import engine
import telethon

async def get(client):
    dialogs = await client.get_dialogs()
    for i in range(len(dialogs)):
        
        if(type(dialogs[i].message.peer_id)==telethon.tl.types.PeerChannel):
            print(dialogs[i].message.peer_id)
            await insert_user_channel(dialogs[i].message.peer_id.channel_id,i)
        else:
            print(dialogs[i].message.peer_id)
            print(dialogs[i].message.peer_id.user_id)
            await insert_user_channel(dialogs[i].message.peer_id.user_id,i)
            
        #messages = await client.get_messages(dialogs[i].id,limit=400)
        #for message in messages:
            #print(message.message)
            #print("\n")
    
async def insert_user_channel(input_channel,input_pri):
    ### find if it exists
    with Session(engine) as session:
        exist = session.query(channels)\
        .filter(channels.user_id=="1")\
        .filter(channels.channel_id==str(input_channel))\
        .all()
        
        if(len(exist)<1):
            
            star_channel = model.channels(user_id="1",priority=input_pri,channel_id=str(input_channel),message="")
            session.add(star_channel)
            session.commit()
            return
        
        
        for row in exist:   
            print(row.user_id, end=" ")
            print(row.channel_id, end=" ")
            print(row.priority)
        
        print("\n")
        
        