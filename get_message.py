async def get_channel_message(client,channel_id):
     msgs = await client.get_messages(channel_id,limit=400)
     for msg in msgs:
         print(msg.message)
         print('\n')