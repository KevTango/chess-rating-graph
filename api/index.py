import os
import berserk
import numpy as np
import datetime as DT
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from flask import Flask, render_template
from enum import Enum

LICHESS_API_TOKEN = os.getenv("LICHESS_API_TOKEN")
LICHESS_USERNAME = os.getenv("LICHESS_USERNAME")
#print(f"Lichess Username: {LICHESS_USERNAME}")

session = berserk.TokenSession(LICHESS_API_TOKEN)
client = berserk.Client(session=session)

# extract JSON data from lichess
ratings_json = client.users.get_rating_history(LICHESS_USERNAME)

# create enum for each lichess type
class LichessRatingType(Enum):
    BULLET = 0
    BLITZ = 1
    RAPID = 2
    CLASSICAL = 3
    CORRESPONDENCE = 4
    CHESS960 = 5
    KING_OF_THE_HILL = 6
    THREE_CHECK = 7
    ANTICHESS = 8
    ATOMIC = 9
    HORDE = 10
    RACING_KINGS = 11
    CRAZYHOUSE = 12
    PUZZLES = 13
    ULTRABULLET = 14

def plot_lichess_results(mode):
    for i in range(len(LichessRatingType)):
        # read list output from JSON
        ratings_list = ratings_json[LichessRatingType(i).value]['points']

        # will only output non null data
        if (not(len(ratings_list))):
            continue

        # will not show puzzle ratings (comment out if needed)
        if (LichessRatingType(i).value == LichessRatingType.PUZZLES.value):
            continue
        
        # extract data and append to array
        date_array = np.array([])
        rating_array = np.array([])

        for x in range(len(ratings_list)):
            date_array = np.append(date_array, [DT.date(ratings_list[x][0], ratings_list[x][1]+1, ratings_list[x][2])])
            rating_array = np.append(rating_array, [ratings_list[x][3]])

        date_array = date_array.astype(DT.date)
        
        if (mode == 0):
            ax.plot(date_array, rating_array, label=f"Lichess {LichessRatingType(i).name} Rating")
        elif (mode == 1):
            ax1.plot(date_array, rating_array, label=f"Lichess {LichessRatingType(i).name} Rating")
        elif (mode == 2):
            ax2.plot(date_array, rating_array, label=f"Lichess {LichessRatingType(i).name} Rating")

# plot default graph
fig, ax = plt.subplots()
plot_lichess_results(0)
ax.legend()
plt.title('Chess Rating History')
plt.xlabel('Date')
plt.ylabel('Rating')

# format x-axis e.g. Jan 2020
xfmt = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_formatter(xfmt)
fig.autofmt_xdate()

fig.savefig('api/static/chess_rating_graph.svg')

# plot dark mode graph
fig1, ax1 = plt.subplots(facecolor='#151515')
plot_lichess_results(1)
ax1.legend()
ax1.set_facecolor('#151515')
plt.title('Chess Rating History', color = '#ffffff')
plt.xlabel('Date', color = '#ffffff')
plt.ylabel('Rating',  color = '#ffffff')
ax1.tick_params(labelcolor='#9f9f9f')

# format x-axis e.g. Jan 2020
xfmt1 = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_formatter(xfmt1)
fig1.autofmt_xdate()

fig1.savefig('api/static/chess_rating_graph_dark.svg')

# plot tokyo night mode graph
fig2, ax2 = plt.subplots(facecolor='#1a1b27')
plot_lichess_results(2)
ax2.legend()
ax2.set_facecolor('#1a1b27')
plt.title('Chess Rating History', color = '#70a5fd')
plt.xlabel('Date', color = '#70a5fd')
plt.ylabel('Rating',  color = '#70a5fd')
ax2.tick_params(labelcolor='#38bdae')

# format x-axis e.g. Jan 2020
xfmt2 = mdates.DateFormatter('%b %Y')
ax2.xaxis.set_major_formatter(xfmt2)
fig2.autofmt_xdate()

fig2.savefig('api/static/chess_rating_graph_tokyo.svg')

#plt.show()

app = Flask(__name__)

@app.route('/')
def graph():
    return render_template('graph.html')

@app.route('/dark')
def dark():
    return render_template('graph_dark.html')

@app.route('/tokyo')
def tokyo():
    return render_template('graph_tokyo.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT") or 5000)