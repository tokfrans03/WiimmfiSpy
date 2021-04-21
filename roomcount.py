from WiimmfiSpy import Room

url = "https://wiimmfi.de/stats/mkw"
url = "https://wiimmfi.de/stats/mkwx/room/p600362544" # brooter
url = "https://wiimmfi.de/stats/mkwx/room/p600345401" # mig
#url = "https://wiimmfi.de/stats/mkwx/room/p600371719" # bii
# url = "https://wiimmfi.de/stats/mkwx/room/r2405987" 

def on_update(r: Room):
    p = len(r.players)
    if p < 12:
        print(p, "< 12")
    else:
        print(p)

r = Room("https://wiimmfi.de/stats/mkwx/room/r2582809")
r.get_forever(on_update)



# ratings = [int(n) for n in [x.vp for x in players] if n != "—"]
# stat = sum(ratings)/len(ratings)

# with open("stats.txt", "a") as f:
#     f.write(str(round(stat)) + "," + str(int(time())) + "\n")

# print(soup.find_all("tr", id=re.compile("r.+")))
# print(len(soup.find_all("tr", id=re.compile("r.+"))))
