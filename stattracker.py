from bs4 import BeautifulSoup
import requests
import re
from player import player
from time import time

players = []

url = "https://wiimmfi.de/stats/mkw"
url = "https://wiimmfi.de/stats/mkwx/room/p600345401"

fp = requests.get(url).text
soup = BeautifulSoup(fp, "html.parser")
rooms = soup.find_all("tr", id=re.compile("r.+"))

for room in rooms:
    for tag in room.next_siblings:
        if tag != "\n":
            if not tag.attrs:
                continue # header
            if "id" in tag.attrs:
                break # new room

            items = [x for x in tag.contents if x != "\n"]
                
            fc = items[0].text.replace("\n", "")
            vp = items[6].text.replace("\n", "")
            bp = items[7].text.replace("\n", "")
            name = tag.find("span", class_="mii-font").string


            players.append(player(fc, vp, bp, name))

print(len(players))

# ratings = [int(n) for n in [x.vp for x in players] if n != "—"]
# stat = sum(ratings)/len(ratings)

# with open("stats.txt", "a") as f:
#     f.write(str(round(stat)) + "," + str(int(time())) + "\n")

# print(soup.find_all("tr", id=re.compile("r.+")))
# print(len(soup.find_all("tr", id=re.compile("r.+"))))