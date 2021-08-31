from typing import Optional, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Room(BaseModel):
    roomName: str
    votes: List[int]


rooms = []

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
            room.votes = []
            return room
    r = Room(roomName = roomName, votes = [])
    rooms.append(r)
    return r


@app.post("/vote")
def vote(vote: int, roomName: str):
    for room in rooms:
        if room.roomName == roomName:
            room.votes.append(vote)


@app.get("/room")
def getRooms(roomName: str):
    for room in rooms:
        if room.roomName == roomName:
            return room.votes
