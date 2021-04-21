import asyncio
from os import waitpid
import threading
from bs4 import BeautifulSoup
import requests
import re
from player import player
from time import sleep
import json

# http://wiki.tockdom.com/wiki/Player_Rating

class Room:
    def __init__(self, url) -> None:
        self.url = url
        self.players = []
        self.metadata = {}
        self.stop = False
        self.sleep = 5

    async def get_forever_async(self, cb):
        while 1:
            print("Getting room...")
            if self.stop:
                break
            self.get()
            await cb(self)
            await asyncio.sleep(self.sleep)

    def get_forever(self, cb):
        while 1:
            if self.stop:
                break
            self.get()
            cb(self)
            sleep(self.sleep)


    def get(self):
        players = []

        fp = requests.get(self.url).text
        soup = BeautifulSoup(fp, "html.parser")
        rooms = soup.find_all("tr", id=re.compile("r.+"))

        try:
            metadata = list(rooms[0].next.strings)
            for data, label in zip(metadata, [None, "id", "age", "type", "cc", ("Match", "duration"), "Lag/Track"]):
                if label == None:
                    continue

                if label == "age":
                    data = data.strip().split()[1]
                elif label == "cc":
                    data = data[-5:]
                    if data == "irror":
                        data = "Mirror"
                elif label == ("Match", "duration"):
                    self.metadata[label[0]] = data.split(" ")[1].replace("#", "")
                    label = label[1]
                    data = data.strip().split(" ")[-2]
                elif label == "Lag/Track":
                    if len(metadata) == 11: # theres lag
                        self.metadata["Lag"] = data.strip()
                    label = "Track"
                    data = metadata[-3]

                self.metadata[label] = data.strip()
        except IndexError:
            print("Empty room")

        for room in rooms:
            for tag in room.next_siblings:
                if tag != "\n":
                    if not tag.attrs:
                        continue  # header
                    if "id" in tag.attrs:
                        break  # new room

                    items = [x for x in tag.contents if x != "\n"]

                    fc = items[0].text.replace("\n", "")
                    try:
                        vp = int(items[5].text.replace("\n", ""))
                    except:
                        vp = items[5].text.replace("\n", "")
                    combo = items[6].text.replace("\n", "")
                    time = items[9].text.replace("\n", "")
                    name = tag.find("span", class_="mii-font").string
                    if not name: # 2 player mode
                        names = list(
                            tag.find("span", class_="mii-font").strings)
                        times = list(items[-2].strings)
                        players.append(player(fc, vp, combo, names[0], times[0]))
                        players.append(player("Guest", 5000, combo, names[1], times[1]))
                    else:
                        players.append(player(fc, vp, combo, name, time))
        self.players = players
        return players

    def dump(self):
        out = {
            "url": self.url,
            "metadata": self.metadata,
            "players": []
        }
        for p in self.players:
            out["players"].append(p.dict())
        return out

    def __repr__(self) -> str:
        return f"Room({self.url}) with {len(self.players)} players"

    def __str__(self) -> str:
        return f"Room({self.url.split('/')[-1]}) with {len(self.players)} players"

if __name__ == "__main__":
    room = Room("https://wiimmfi.de/stats/mkwx/room/r2592523")
    room.get()
    print(room)
    print(room.dump())
