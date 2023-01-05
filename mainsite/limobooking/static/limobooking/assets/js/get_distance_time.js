function initMap() {
  var origine = "17 Rue nationale, 60540 Belle-Église, France";
  var destination = document.getElementById("destination").textContent;
  var service = new google.maps.DistanceMatrixService;
  service.getDistanceMatrix({
    origins: [origine],
    destinations: [destination],
    travelMode: 'DRIVING',
    unitSystem: google.maps.UnitSystem.METRIC,
    avoidHighways: false,
    avoidTolls: false
  }, function(response, status) {
    if (status !== 'OK') {
      alert('Error was: ' + status);
    } else {
      var originList = response.originAddresses;
      var destinationList = response.destinationAddresses;
      var laDistance = document.getElementById("laDistance");
      var resultat = response.rows[0].elements;
      var distance = resultat[0].distance['value'];
	    laDistance.innerHTML = resultat[0].distance.text + ", pour une durée de trajet estimée à " + 
        resultat[0].duration.text ;
	    document.getElementById("distance").value = distance;
    }
  });
}	
