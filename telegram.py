from turtle import back
from telethon import TelegramClient,events,functions
import telethon
import asyncio
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

async_mode = None
client = None
t = None
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
    emit('my_response',{'data':'connect using phone:'})
    print('connected')


@socketio.on('my_event')
def handle_my_event(mes):
    print(mes)

@app.route('/')
def index():
    return render_template('./src/index2.html',async_mode='eventlet')

@socketio.on('message')
def handle_message(message):
    print("out",end="")
    print(message)
    ## te
    socketio.sleep(.1)
    emit('my_response',{'data':message['data']})
    eventlet.sleep(0)
    socketio.sleep(.1)

def background_thread():
    async def go():
        global client
        global phone
        if phone=="":
            return
        socketio.sleep(.1)
        socketio.emit('my_response',{'data':'connecting ... '})
        try:
            client = TelegramClient(phone,api_id,api_hash)
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(phone)
                code = input("mycode: ")
                if(code!=""):
                    me = await client.sign_in(phone,input("mycode: "))
            #print((await client.get_me()).stringify())
            socketio.emit('my_response',{'data':'connected!'})
            me = await client.get_me()
            socketio.emit('my_response',{'data':me.first_name+' '+me.last_name})
            ### get all the friends(channels) and the content of it  
            await get_dialog.get(client)

            listen.listen(client,socketio)      
            await client.run_until_disconnected()
        except:
            print("ERR CONNECT")
    asyncio.run(go())

def test_thread():
    print("test_thread")
    async def work():
        global client
        global phone
        if phone=="":
            return
        print("work")
        socketio.sleep(.1)
        socketio.emit('my_response',{'data':'phone : ' + phone})
        try:
            client = TelegramClient(phone,api_id,api_hash)
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(phone)
                code = input("mycode: ")
                if(code!=""):
                    me = await client.sign_in(phone,input("mycode: "))
            socketio.emit('my_response',{'data':'connected!'})
           
            me = await client.get_me()
            
            
            ### listening on the message , print out the sender channel
            while True:
                socketio.sleep(1)
                print("in while")
                @client.on(events.NewMessage())
                async def event_handelr(evt):
                    global tmpID
                    global PID
                    channel = await evt.get_chat()
                    print("listening")
                    
                    msgs =(await client.get_messages(channel.id,limit=1))
                    msg = msgs[0]

                    if(msg.id!=tmpID):
                        print(msg)
                        
                        socketio.sleep(.1)
                        socketio.emit('my_response',{'data':msg.message,'count':channel.id})

                        socketio.sleep(.1)
                    
                    tmpID = msg.id

                    if(type(msg.peer_id)==telethon.tl.types.PeerChannel):
                        PID = msg.peer_id.channel_id
                    elif(type(msg.peer_id)==telethon.tl.types.PeerChat):
                        PID = msg.peer_id.chat_id
                    else:
                        PID = msg.peer_id.user_id

                me = await client.get_me()

            await client.run_until_disconnected()
            ### always running
            
        except (RuntimeError,TypeError,KeyboardInterrupt) as err:
            if(err!=KeyboardInterrupt):
                print(err)
            pass
    asyncio.run(work())
    print("W")

@socketio.on('disconnect_telegram')
def disconnect_telegram():
    async def dis():
        async def fin():
            await client.disconnect()
        await fin()
    print("disconnect")
    emit('my_response',{'data':'disconnecting'})
    socketio.sleep(.1)
    
    asyncio.run(dis())

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
    start_socket()
    
    
    
        
