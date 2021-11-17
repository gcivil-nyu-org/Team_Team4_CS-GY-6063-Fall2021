function showPosition() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      document.getElementById("longitude").value = position.coords.longitude;
      document.getElementById("latitude").value = position.coords.latitude;
      document.getElementById("result").innerHTML =
        position.coords.longitude + ", " + position.coords.latitude;
      const map = document.getElementById("map");
      map.setCenter(
        new google.maps.LatLng(
          position.coords.latitude,
          position.coords.longitude
        )
      );
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
    // document.getElementById("locationInput").disabled = false;
  }
  // document.getElementById("locationLoading").innerText = "";
}
