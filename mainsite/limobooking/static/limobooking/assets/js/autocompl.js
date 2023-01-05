
document.getElementById('autocomplete').focus();		
var defaultBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(49.615582,-1.769906), new google.maps.LatLng(43.269854,5.942125)
);
var options = { bounds: defaultBounds };
function activatePlacesSearch(){
	var input = document.getElementById('autocomplete');
	var autocomplete = new google.maps.places.Autocomplete(input, options);
} 
