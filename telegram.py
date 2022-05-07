from asyncio.windows_events import NULL
from pydoc import cli
from turtle import back
from telethon import TelegramClient,events,functions
import telethon
import asyncio
from unsync import unsync
import dbconfig,psycopg2,listen,get_dialog
import get_message
from telethon.tl.functions.users import GetFullUserRequest
import threading
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import time
import multiprocessing as mp
import eventlet
import DB

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
    print("test_thread")
    async def work():
        global client
        global phone
        if phone=="":
            return
        print("work")
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
            socketio.emit('my_response',{'data':'connected!','count':'System'})
            await client.send_message('me','conn')
            #await get_dialog.get(client)
            
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
                        print(tmpID)
                        print(msg.id)
                        tmpID = msg.id
                        socketio.sleep(.1)
                        socketio.emit('my_response',{'data':msg.message,'count':channel.id})
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
    
    
    
        
