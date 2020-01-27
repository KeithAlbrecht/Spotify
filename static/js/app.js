spotify_track = ''

function PredictionFunction(spotify_track) {
  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 'key': spotify_track })
  }).then((response, d) => console.log(response));
}


d3.selectAll(".btn").on("click", function (d, i) {
  spotify_track = this.name
})

