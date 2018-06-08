var heatmap_layer;
var map;

var daysAllowed = {
    "Monday": false,
    "Tuesday": false,
    "Wednesday": false,
    "Thursday": false,
    "Friday": false,
    "Saturday": false,
    "Sunday": false
};

var typesAllowed = {
    "Unknown Injuries": false,
    "No Injuries": false,
    "Injuries": false,
    "Delayed": false,
    "Entrapment": false
};

var timesAllowed = {
    "00:00-00:59": false,
    "01:00-01:59": false,
    "02:00-02:59": false,
    "03:00-03:59": false,
    "04:00-04:59": false,
    "05:00-05:59": false,
    "06:00-06:59": false,
    "07:00-07:59": false,
    "08:00-08:59": false,
    "09:00-09:59": false,
    "10:00-10:59": false,
    "11:00-11:59": false,
    "12:00-12:59": false,
    "13:00-13:59": false,
    "14:00-14:59": false,
    "15:00-15:59": false,
    "16:00-16:59": false,
    "17:00-17:59": false,
    "18:00-18:59": false,
    "19:00-19:59": false,
    "20:00-20:59": false,
    "21:00-21:59": false,
    "22:00-22:59": false,
    "23:00-23:59": false
};

function update_type() {
    var selectVals = $('#type_dropdown').val();

    typesAllowed = {
        "Unknown Injuries": false,
        "No Injuries": false,
        "Injuries": false,
        "Delayed": false,
        "Entrapment": false
    };
    for (var i in selectVals) {
        typesAllowed[selectVals[i]] = true;
    }
}

function update_day() {
    var selectVals = $('#day_dropdown').val();
    daysAllowed = {
        "Monday": false,
        "Tuesday": false,
        "Wednesday": false,
        "Thursday": false,
        "Friday": false,
        "Saturday": false,
        "Sunday": false
    };
    for (var i in selectVals) {
        daysAllowed[selectVals[i]] = true;
    }
}

function update_time() {
    var selectVals = $('#timeframe_dropdown').val();
    timesAllowed = {
        "00:00-00:59": false,
        "01:00-01:59": false,
        "02:00-02:59": false,
        "03:00-03:59": false,
        "04:00-04:59": false,
        "05:00-05:59": false,
        "06:00-06:59": false,
        "07:00-07:59": false,
        "08:00-08:59": false,
        "09:00-09:59": false,
        "10:00-10:59": false,
        "11:00-11:59": false,
        "12:00-12:59": false,
        "13:00-13:59": false,
        "14:00-14:59": false,
        "15:00-15:59": false,
        "16:00-16:59": false,
        "17:00-17:59": false,
        "18:00-18:59": false,
        "19:00-19:59": false,
        "20:00-20:59": false,
        "21:00-21:59": false,
        "22:00-22:59": false,
        "23:00-23:59": false
    };
    for (var i in selectVals) {
        timesAllowed[selectVals[i]] = true;
    }
}

function initPage() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: new google.maps.LatLng(35.0479, -85.2960)
    });
    heatmap_layer = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
    });
    heatmap_layer.setMap(map);
    $('#timeframe_dropdown')
        .dropdown()
    ;
    $('#type_dropdown')
        .dropdown()
    ;
    $('#day_dropdown')
        .dropdown()
    ;
}

function update_points() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: new google.maps.LatLng(35.0479, -85.2960)
    });
    heatmap_layer.setMap(null)
    heatmap_layer = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
    });
    heatmap_layer.setMap(map);
}

function getPoints() {
    var points = [];
    var request = new XMLHttpRequest();
    request.open("GET", "https://gist.githubusercontent.com/oitsjustjose/278800f898380a8212bb6b78919c0833/raw/64be83d6a5d00d57ab8595e3e61c15242b124c51/data.csv", true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                var spl = request.responseText.split("\n");
                for (var i in spl) {
                    // Ignore lines that are empty:
                    if (spl[i].indexOf(",") === -1) {
                        continue;
                    }
                    var day = spl[i].split(",")[2].substring(1);
                    var time = spl[i].split(",")[5];
                    var reportType = spl[i].split(",")[6].substring(1);
                    if (!daysAllowed[day]) {
                        continue;
                    }
                    if (!typesAllowed[reportType]) {
                        continue;
                    }
                    if (!isWithinTimeRange(time)) {
                        continue;
                    }
                    var lat = spl[i].split(",")[0];
                    var lon = spl[i].split(",")[1];
                    points[i] = new google.maps.LatLng(parseFloat(lat), parseFloat(lon));
                }
                heatmap_layer.setMap(map);
            }
        }
    };
    return points;
}

function isWithinTimeRange(time) {
    var hour = parseInt(time.split(":")[0]);
    var minute = parseInt(time.split(":")[1]);
    for (var i in timesAllowed) {
        var hourStart = parseInt(i.split("-")[0].split(":")[0]);
        var minuteStart = parseInt(i.split("-")[0].split(":")[1]);
        var hourEnd = parseInt(i.split("-")[1].split(":")[0]);
        var minuteEnd = parseInt(i.split("-")[1].split(":")[1]);

        if (hourStart <= hour && hour <= hourEnd) {
            if (minuteStart <= minute && minute <= minuteEnd) {
                return timesAllowed[i];
            }
        }
    }
    return false;
}


function getIndex(date) {
    if (date.indexOf("Monday") !== -1) {
        return 0;
    }
    if (date.indexOf("Tuesday") !== -1) {
        return 1;
    }
    if (date.indexOf("Wednesday") !== -1) {
        return 2;
    }
    if (date.indexOf("Thursday") !== -1) {
        return 3;
    }
    if (date.indexOf("Friday") !== -1) {
        return 4;
    }
    if (date.indexOf("Saturday") !== -1) {
        return 5;
    }
    if (date.indexOf("Sunday") !== -1) {
        return 6;
    }
}