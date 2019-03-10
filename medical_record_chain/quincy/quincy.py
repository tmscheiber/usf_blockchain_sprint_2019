from sanic import Sanic
import socketio
from sqlalchemy.orm import sessionmaker
from models import engine
from models import QSpace
import os

environment = os.environ.get("environment", "development")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

sio = socketio.AsyncServer(async_mode="sanic")
app = Sanic()
sio.attach(app)

@sio.on("connect")
async def connect(sid, environ, *args, **kwargs):
    print(f"socket connected with sid {sid}")
    qspace = session.query(QSpace).filter_by(qspace='dan').first()

    if qspace:
        await sio.emit('canvasChanged', data = qspace.data)

@sio.on("canvasChanged")
async def new_star(sid, data):
    await sio.emit('canvasChanged', data=data, skip_sid=True)

# save the current state to the database
@sio.on("saveToDatabase")
async def save(sid, data):
    print(data)
    qspace = session.query(QSpace).filter_by(qspace='dan').first()

    if not qspace:
        qspace = QSpace(qspace='dan', data=data)

    qspace.data = data
    session.add(qspace)
    session.commit()

@sio.on("loadFromDatabase")
async def load(sid):
    qspace = session.query(QSpace).filter_by(qspace='dan').first()
    await sio.emit('canvasChanged', data = qspace.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
