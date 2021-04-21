import matplotlib.pyplot as plt
# import matplotlib.dates as md
from datetime import datetime
import numpy as np

with open("stats.txt") as f:
    aaa = f.readlines()

x = [datetime.fromtimestamp(int(x.split(",")[1])) for x in aaa]
y = [int(y.split(",")[0]) for y in aaa]


# t = np.arange(x[0], x[-1], 60.1)
# fig, ax = plt.subplots()

# ky = ax.plot(t, x, label='x')
# ky2 = ax.plot(t, y, label='y')

# # plotting the points  
plt.plot(x, y)
  
# naming the x axis 
plt.xlabel('x - axis') 
# naming the y axis 
plt.ylabel('y - axis') 
  
# giving a title to my graph 
plt.title('Medel Versus Point över tid') 

ax=plt.gcf().autofmt_xdate()

# xfmt = md.DateFormatter('%H:%M:%S')
# ax.xaxis.set_major_formatter(xfmt)
  
# function to show the plot 
plt.show()