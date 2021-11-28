function showPosition() {
  if (navigator.geolocation) {
    document.getElementById(
      "locationLoading"
    ).innerHTML = `<i class="fas fa-spinner mr-3"></i>Getting your location...`;
    document.getElementById("searchLocation").disabled = true;
    navigator.geolocation.getCurrentPosition(function (position) {
      document.getElementById("longitude").value = position.coords.longitude;
      document.getElementById("latitude").value = position.coords.latitude;
      document.getElementById("locationLoading").innerHTML = "";
      document.getElementById("searchLocation").disabled = false;
    });
  } else {
    alert("Sorry, your browser does not support HTML5 geolocation.");
  }
}

function toggleCurrentLocation() {
  var currentLocation = document.getElementById("useCurrentLocation");
  if (currentLocation.checked) {
    showPosition();
    currentLocation.value = "true";
  } else {
    currentLocation.value = "false";
    document.getElementById("locationLoading").innerHTML = "";
    document.getElementById("searchLocation").disabled = false;
  }
}
