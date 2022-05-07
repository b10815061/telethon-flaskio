from ast import expr_context
from asyncio.windows_events import NULL
import base64
from io import BytesIO
from pydoc import cli
from PIL import Image
from turtle import back
from telethon import TelegramClient,events,functions
import telethon
import asyncio
from unsync import unsync
import dbconfig,psycopg2,listen,get_dialog
import get_message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerUser
from util import utils
import threading
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import time
import multiprocessing as mp
import eventlet
import DB
import os

async_mode = None
client = None
t = None
code =""
phone = ""

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
tmpID = ""
PID = ""

api_id = 12655046
api_hash = 'd84ab8008abfb3ec244630d2a6778fc6'
image_path = "images"


@socketio.event
def connect():
    emit('my_response',{'data':'Enter phone to start','count':'System'})
    print('connected')


@socketio.on('my_event')
def handle_my_event(mes):
    print(mes)

@app.route('/')
def index():
    return render_template('./src/index2.html',async_mode='eventlet')

@socketio.on('message')
def handle_message(message):
    print(message)
    if(message['cid']=="Code"):
        global code
        code = message['data']
        print(code)
    elif client!=None and client.is_connected():
        @unsync
        async def send():
            socketio.sleep(.1)
            await client.send_message(str(message['cid']),message['data'])
            socketio.sleep(.1)
        socketio.sleep(.1)
        send()
        
    else:
        emit('my_response',{'data':'not connected!','count':'System'})
    socketio.sleep(.1)

def test_thread():
    async def work():
        global client
        global phone
        if phone=="":
            return
        socketio.sleep(.1)
        socketio.emit('my_response',{'data':'phone : ' + phone,'count':'System'})
        try:
            client = TelegramClient(phone,api_id,api_hash)
            await client.connect()
            socketio.sleep(.1)

            if not await client.is_user_authorized():
                socketio.sleep(.1)
                await client.send_code_request(phone)
                socketio.sleep(.1)
                socketio.emit('my_response',{'data':'please enter code in the message field','count':'System'})
                socketio.sleep(.1)
                while code=="":
                    socketio.sleep(3)
                    print("code : " + code)
                await client.sign_in(phone,code)
            me = await client.get_me()
            socketio.emit('my_response',{'data':'connected!','count':'System'})
            await client.send_message('me','conn')
            await get_dialog.get(client)

            chan = await get_dialog.retrive_all(me.id)

            for c in chan :
                print(c.channel_id)
                try:
                    with open(f'./images/{c.channel_id}.png','rb')as f:
                            image_data = f.read()
                            socketio.sleep(.1)
                            b64 = base64.b64encode(image_data).decode()
                            chat_id = c.channel_id
                            try:
                                user_name = (await client.get_entity(int(chat_id))).title
                                print(user_name)
                                pri = await get_dialog.retrive_prior(me.id,chat_id)

                            except:
                                U = await client.get_entity(int(chat_id))
                                user_name = utils.name2str(U.first_name) + " " + utils.name2str(U.last_name)
                                pri = await get_dialog.retrive_prior(me.id,chat_id)
                                print(f'cannot get {chat_id}')
                            socketio.sleep(.1)
                            socketio.emit('image',{'data':b64,'name':user_name,'pri':pri})
                            socketio.sleep(.1)
                            print(f'{c.channel_id} sent')
                except:
                    print("not found image")
                print("DONE SENDING IMAGE")

           
            
            ### listening on the message , print out the sender channel
            while client.is_connected():
                socketio.sleep(1)
                @client.on(events.NewMessage())
                async def event_handelr(evt):
                    global tmpID
                    global PID
                    channel = await evt.get_chat()
                    
                    msgs =(await client.get_messages(channel.id,limit=1))
                    msg = msgs[0]
                    
                    if(msg.id!=tmpID):
                        print(f'CHANNEL ID : {channel.id}')
                        print(f'MSG {msg}')
                        print(tmpID)
                        print(msg.id)
                        tmpID = msg.id
                        client.parse_method = 'html'
                        print(msg)
                        socketio.sleep(.1)
                        try:    
                            rtnName = channel.title
                        except:
                            rtnName = channel.id
                        socketio.emit('my_response',{'data':msg.message,'count':rtnName})
                        socketio.sleep(.1)
                    
                    

                    if(type(msg.peer_id)==telethon.tl.types.PeerChannel):
                        PID = msg.peer_id.channel_id
                    elif(type(msg.peer_id)==telethon.tl.types.PeerChat):
                        PID = msg.peer_id.chat_id
                    else:
                        PID = msg.peer_id.user_id
                if(client.is_connected()):
                    me = await client.get_me()

            #await client.run_until_disconnected()
            ### always running
            
        except (RuntimeError,TypeError,KeyboardInterrupt) as err:
            if(err!=KeyboardInterrupt):
                print(err)
            pass
    asyncio.run(work())

@socketio.on('disconnect_telegram')
def disconnect_telegram():
    @unsync
    async def dis():
        socketio.sleep(.1)
        await client.disconnect()
        socketio.sleep(.1)
        print("disconnect")
    emit('my_response',{'data':'disconnecting','count':'System'})
    socketio.sleep(.1)
    dis()

@socketio.on('connect_to_telegram')
def handler_connect_to_telegram(message):
    global phone
    phone = message['data']
    global thread
    with thread_lock:
        thread = socketio.start_background_task(test_thread)
    

def start_socket():
    socketio.run(app)
    print('after')


if __name__ == '__main__':
    #asyncio.run(DB.get_pri())
    start_socket()
    
    
    
        
