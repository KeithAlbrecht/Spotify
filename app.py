import os
import sqlite3
import pandas as pd
import numpy as np
import random
import pickle

from flask import Flask, jsonify, render_template

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

# @app.route("predict")
# def PredictionFunction():

# slacked from Chris...
@app.route('/', methods=['GET','POST'])
def predict():
    genre = ''
    if request.method == 'POST':
        popularity = float(request.form["popularity"])
        acousticness = float(request.form["acousticness"])
        danceability = float(request.form["danceability"])
        energy = float(request.form["energy"])
        instrumentalness = float(request.form["instrumentalness"])
        loudness = float(request.form["loudness"])
        liveness = float(request.form["liveness"])
        speechiness = float(request.form["speechiness"])
        tempo = float(request.form["tempo"])
        valence = float(request.form["valence"])
        duration_ms = float(request.form["duration_ms"])
        data = np.array([popularity, acousticness, danceability, energy, instrumentalness, loudness, liveness, speechiness, tempo, valence, duration_ms]).reshape(1,-1)
        results = int(clf.predict(data)[0])
        genre = f"{results:,}"
    return render_template("form.html", genre=genre)
if __name__ == "__main__":
    clf = joblib.load('model.pkl')
    app.run()


# if __name__ == "__main__":
#     app.run()

