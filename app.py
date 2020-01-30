import os
import sqlite3
import pandas as pd
import numpy as np
import random
import pickle
import json

from flask import Flask, jsonify, render_template
from flask import request
from sklearn.externals import joblib
with open('decade_model.pkl', 'rb') as f:
    model = joblib.load(f)
with open('scaler.pkl', 'rb') as f:
    X_scaler = joblib.load(f)
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

#################################################
# Database Setup
#################################################

conn = sqlite3.connect('spotify_db.sqlite')
db = pd.read_sql('select * from spotify_db', conn)

spotify_joblib_model = joblib.load('decade_model.pkl')
spotify_db = db.copy()
image_url_list=list(zip(spotify_db["Image URL"],spotify_db["URI"]))
@app.route("/")
def index():
    
    # print(image_url_list)
    # for i in range(10):
    #     image_url_list.append(spotify_db["Image URL"][random.randint(0,len(spotify_db["Image URL"]))])
    random.shuffle(image_url_list)
    return render_template("index.html",image_urls=image_url_list[0:30])


@app.route("/tracks/<spotify_track>")
def tracks(spotify_track):
    print(spotify_db)
    x = spotify_db[spotify_db["URI"] == spotify_track]
    print(x)
    for column in x.columns:
        print(column)
    
    popularity = x.iloc[0, 6]
    acousticness = x.iloc[0, 7]
    danceability = x.iloc[0, 8]
    energy = x.iloc[0, 9]
    instrumentalness = x.iloc[0, 10]
    loudness = x.iloc[0, 11]
    speechiness = x.iloc[0, 12]
    tempo = x.iloc[0, 13]
    valence = x.iloc[0, 14]
    duration_ms = x.iloc[0, 15]

    artist_name = x.iloc[0,2]
    track_name = x.iloc[0,3]
    actual_decade = x.iloc[0,4]
    
    print(spotify_track)
    data = np.array([popularity, acousticness, danceability, energy, instrumentalness, loudness, speechiness, tempo, valence, duration_ms]).reshape(1,-1)
    print(data)
    print(track_name)
    print(artist_name)
    
    data_scaled = X_scaler.transform(data)

    prediction = spotify_joblib_model.predict(data_scaled)    
    print(prediction)
    print(prediction[0])
    # return jsonify(int(prediction[0]))
    return jsonify({"prediction":int(prediction[0]),
    "actual":int(float(actual_decade))})

@app.route("/predict", methods=['POST'])
def PredictionFunction():
    data_dict = json.loads(request.data.decode('utf-8'))
    spotify_track=data_dict["key"]
    print(spotify_track)
    return 'this is data'

if __name__ == "__main__":
    app.run()

