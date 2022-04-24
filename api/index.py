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

# read list output from JSON
rapid_ratings_list = ratings_json[LichessRatingType.RAPID.value]['points']

# extract data and append to array
rapid_date_array = np.array([])
rapid_rating_array = np.array([])

for i in range(len(rapid_ratings_list)):
    rapid_date_array = np.append(rapid_date_array, [DT.date(rapid_ratings_list[i][0], rapid_ratings_list[i][1]+1, rapid_ratings_list[i][2])])
    rapid_rating_array = np.append(rapid_rating_array, [rapid_ratings_list[i][3]])

rapid_date_array = rapid_date_array.astype(DT.date)

# plot data
fig, ax = plt.subplots()
ax.plot(rapid_date_array, rapid_rating_array, label="Lichess Rapid Rating")
ax.legend()
plt.xlabel('Date')
plt.ylabel('Rating')
plt.title('Chess Rating History')

# format x-axis e.g. Jan 2020
xfmt = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_formatter(xfmt)
fig.autofmt_xdate()

# save graph
fig.savefig('api/static/chess_rating_graph.svg')

# plt.show()

app = Flask(__name__)

@app.route('/')
def graph():
    return render_template('graph.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT") or 5000)