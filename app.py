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
    
    popularity = x.iloc[0, 3]
    acousticness = x.iloc[0, 4]
    danceability = x.iloc[0, 5]
    energy = x.iloc[0, 6]
    instrumentalness = x.iloc[0, 7]
    loudness = x.iloc[0, 8]
    speechiness = x.iloc[0, 9]
    tempo = x.iloc[0, 10]
    valence = x.iloc[0, 11]
    duration_ms = x.iloc[0, 12]
    print(spotify_track)
    data = np.array([popularity, acousticness, danceability, energy, instrumentalness, loudness, speechiness, tempo, valence, duration_ms]).reshape(1,-1)
    print(data)
    
    X_scaler = StandardScaler().fit(data)

    data_scaled = X_scaler.transform(data)

    prediction = spotify_joblib_model.predict(data_scaled)    
    print(prediction)
    print(prediction[0])
    return jsonify(int(prediction[0]))

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

