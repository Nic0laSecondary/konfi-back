from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Room(BaseModel):
    roomName: str
    privateVotes: dict

    def get_votes(self):
        toReturn = []
        toReturn.extend(self.privateVotes.values())
        return toReturn


rooms = []
cookie_string: str = "KonfiDenceVoteCookie"
global cookie_count
cookie_count: int = 0

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def getRooms():
    return rooms


@app.get("/test/")
def do_test():
    return "Super complex String message"


@app.post("/add/")
def addRoom(roomName: str):
    for room in rooms:
        if room.roomName == roomName:
            room.privateVotes = {}
            return room
    r = Room(roomName=roomName, privateVotes={})
    rooms.append(r)
    return r


@app.post("/vote")
def vote(vote: int, roomName: str, fakeCookie: int):
    cookieNumber = 0
    if fakeCookie == 0:
        global cookie_count
        cookie_count += 1
        cookieNumber = cookie_count
    else:
        cookieNumber = fakeCookie
    for room in rooms:
        if room.roomName == roomName:
            room.privateVotes[str(cookieNumber)] = vote
    return cookieNumber


@app.get("/room")
def getRooms(roomName: str):
    for room in rooms:
        if room.roomName == roomName:
            return room.get_votes()
