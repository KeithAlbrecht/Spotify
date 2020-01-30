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
    var sel = document.getElementById('decade');
    // console.log(sel.options[sel.selectedIndex].value)
    var user = d3.select("#user");
    var model = d3.select("#model");
    var actual = d3.select("#actual");
    user.text(`Your guess:${sel.options[sel.selectedIndex].value}`);
    model.text(`Model's prediction:${prediction}`);
    actual.text(`Actual:${(actual_decade)}`);
  });    
}