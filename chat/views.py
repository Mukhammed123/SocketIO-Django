# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
import socketio
from django.http import HttpResponse
import os

async_mode = None


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode,
                      cors_allowed_origins=["http://localhost:8080", "http://127.0.0.1:8000"])
thread = None


def index(request):
    print(request)
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(5)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.on("join room one")
def join_event_handler(sid):
    sio.enter_room(sid, 'room_one')
    print("joined")


@sio.event
def my_message(sid, data):
    sio.emit('broad cast reply', data, room='room_one', skip_sid=sid)


@sio.event
def my_event(sid, message):
    print(sid, message)
    sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


# @on_message(channel="room-1")
# def my_chat_handler(request, socket, context, message):
#     print("========= Trying to connect to the room-1 ========")
#     sio.broadcast("Hello everybody!!")


# Frontend
"""
this.socket = new io('http://127.0.0.1:8000/',{transports: [ 'websocket', 'polling' ]});

      this.socket.on("connect", () => {
  const engine = this.socket.io.engine;

  console.log(engine.transport.name); // in most cases, prints "polling"

  engine.once("upgrade", () => {
    console.log("Upgraded")
    // called when the transport is upgraded (i.e. from HTTP long-polling to WebSocket)
    console.log(engine.transport.name); // in most cases, prints "websocket"
  });

  engine.on('my_response', ({type, data}) => {console.log(type, data)} );

  engine.on("packet", ({ type, data }) => {
    // called for each packet received
    console.log(type,data)
  });

  engine.on("packetCreate", ({ type, data }) => {
    // called for each packet sent
    console.log(type,data)
  });

  engine.on("drain", () => {
    // called when the write buffer is drained
    console.log("drain")
  });

  engine.on("close", (reason) => {
    // called when the underlying connection is closed
    console.log(reason)
  });

  engine.on("broad cast reply", ({type, data}) => {
    console.log("From the broadcast")
    console.log(type, data)
  })
  // this.socket.emit("show asdfas", data)
});

joinRoom() {
        this.socket.emit("join room one")
      },
      async addMessage() {
        this.socket.emit("my_message",{data:JSON.stringify({message: this.content, author: this.author})})
        // const response = await axios.post('http://localhost:8000/message/create/', {message: this.content, author: this.author});
        this.content = '';
        this.author = '';
      // console.log(response)
      },
"""
