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

app = Flask(__name__)

#################################################
# Database Setup
#################################################

conn = sqlite3.connect('spotify_db.sqlite')
db = pd.read_sql('select * from spotify_db', conn)

spotify_joblib_model = joblib.load('spotify_model.sav')
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
    
    sel = [
        db.spotify_track,
        db.Popularity,
        db.Acousticness,
        db.Danceability,
        db.Energy,
        db.Instrumentalness,
        db.Loudness,
        db.Speechiness,
        db.Tempo,
        db.Valence,
        db.Duration (ms),
    ]

    results = db.session.query(*sel).filter(db.spotify_track == spotify_track).all()

    # Create a dictionary entry for each row of metadata information
    spotify_track = {}
    for result in results:
        spotify_track["spotify_track"]=result[0]
        spotify_track["Popularity"]=result[4]
        spotify_track["Acousticness"]=result[5]
        spotify_track["Danceability"]=result[6]
        spotify_track["Energy"]=result[7]
        spotify_track["Instrumentalness"]=result[8]
        spotify_track["Loudness"]=result[9]
        spotify_track["Speechiness"]=result[10]
        spotify_track["Tempo"]=result[11]
        spotify_track["Valence"]=result[12]
        spotify_track["Duration (ms)"]=result[13]

    print(spotify_track)
    return jsonify(spotify_track)


@app.route("/predict", methods=['POST'])
def PredictionFunction():
    data_dict = json.loads(request.data.decode('utf-8'))
    spotify_track=data_dict["key"]
    print(spotify_track)
    return 'this is data'

# @app.route("/predict", methods=['GET','POST'])
# def PredictionFunction():
#     decade = ''
#     if request.method =='POST':
#         popularity = float(request.form["popularity"])
#         acousticness = float(request.form["acousticness"])
#         danceability = float(request.form["danceability"])
#         energy = float(request.form["energy"])
#         instrumentalness = float(request.form["instrumentalness"])
#         loudness = float(request.form["loudness"])
#         liveness = float(request.form["liveness"])
#         speechiness = float(request.form["speechiness"])
#         tempo = float(request.form["tempo"])
#         valence = float(request.form["valence"])
#         duration_ms = float(request.form["duration_ms"])
#         data = np.array([popularity, acousticness, danceability, energy, instrumentalness, loudness, liveness, speechiness, tempo, valence, duration_ms]).reshape(1,-1)
#         results = int(spotifyDecade.predict(data)[0])
#         decade = f"{results:,}"
#     return render_template("form.html", decade=decade)
# if __name__ == "__main__":
#     spotifyDecade = joblib.load('spotify_model.pkl')
#     app.run()


# slacked from Chris...
# @app.route('/', methods=['GET','POST'])
# def predict():
#     genre = ''
#     if request.method == 'POST':
#         popularity = float(request.form["popularity"])
#         acousticness = float(request.form["acousticness"])
#         danceability = float(request.form["danceability"])
#         energy = float(request.form["energy"])
#         instrumentalness = float(request.form["instrumentalness"])
#         loudness = float(request.form["loudness"])
#         liveness = float(request.form["liveness"])
#         speechiness = float(request.form["speechiness"])
#         tempo = float(request.form["tempo"])
#         valence = float(request.form["valence"])
#         duration_ms = float(request.form["duration_ms"])
#         data = np.array([popularity, acousticness, danceability, energy, instrumentalness, loudness, liveness, speechiness, tempo, valence, duration_ms]).reshape(1,-1)
#         results = int(clf.predict(data)[0])
#         genre = f"{results:,}"
#     return render_template("form.html", genre=genre)
# if __name__ == "__main__":
#     clf = joblib.load('model.pkl')
#     app.run()


if __name__ == "__main__":
    app.run()

