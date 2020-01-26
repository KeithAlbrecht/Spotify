spotify_track = ''

function PredictionFunction(spotify_track) {
  fetch('/predict', {
    method: 'POST',
    body: {key:spotify_track}
  }).then((response) => console.log(response));
}


d3.selectAll(".btn").on("click", function(d,i){
  spotify_track = this.name
}) 

