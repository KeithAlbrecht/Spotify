spotify_track = ''

d3.selectAll(".btn").on("click", function (d, i) {
  spotify_track = this.name
})

$('#myModal').on('show.bs.modal', function (event) {
  window.SONGID = event.relatedTarget.name;
});
function PredictionFunction() {
  d3.json(`/tracks/${window.SONGID}`).then(function(prediction) {     
    console.log(prediction)
    //DO SOMETHING WITH THE PREDICTION
    
  });    
}
