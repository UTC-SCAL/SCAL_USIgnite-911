function initPage() {
    var center = new google.maps.LatLng(35.0479, -85.2960);
    var options =
        {
            zoom: 20,
            center: center
        };
    var map = new google.maps.Map(document.getElementById("map"), options);

}
