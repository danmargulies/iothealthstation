var ws;
var selectedPatientID = undefined;
var lastDetectedPulse = undefined;
var piechart = {
    type: 'pie',
    options: {
        responsive: false,
        title: {
            display: true,
            text: 'Minimum Temperature per device over the last 10 sec'
        },
    },
    data: {}
}
var barchart = {
    type: 'bar',
    data: {},
    options: {
        responsive: false,
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Average Temperature & Humidity per device the last 10 sec'
        },
        scales: {
            yAxes: [{
                display: true,
                gridLines: {
                    color: "rgb(210,210,211)"
                },
                ticks: {
                    max: 150,
                    min: 0,
                    stepSize: 10,
                    beginAtZero: true,
                    padding: 20,
                    callback: function (value, index, values) {
                        return value// + "k";
                    }
                }
            }]
        }
    }
}


function init() {
    var ctx = document.getElementById("myChart").getContext("2d");
    var ctx2 = document.getElementById("myChart2").getContext("2d");
    //  var myBarChart = new Chart(ctx, barchart);
    // var myPieChart = new Chart(ctx2, piechart);
    ws = new WebSocket("ws://54.92.213.29:9001/"); //modify ip address to match public for server

    // Set event handlers.
    ws.onopen = function () {
        output("onopen");
    };

    ws.onmessage = function (e) {
        if (selectedPatientID === undefined) {
            document.getElementById("patientname").textContent = "Please select a patient from below"
            return
        }

        // e.data contains received string.
        output("onmessage: " + e.data);

        ddata = JSON.parse(e.data)

        var bpmelem = document.getElementById("bpm-1")
        var oxelem = document.getElementById("ox-1")
        //console.log("----- BPM", ddata.AVGBPM, aat[0])
        var patientname = ddata.MSG.split("#")[0] //parses MSG payload from the IoTHealthStation
        var patientmrn = ddata.MSG.split("#")[1]
        if (selectedPatientID != patientmrn) {
            return;
        }
        document.getElementById("patientname").textContent = patientname
        document.getElementById("patientmrn").textContent = patientmrn
        document.getElementById("temp-1").innerHTML = ddata.AVGTEMP + "<span>&#176;</span>"
        document.getElementById("hum-1").innerHTML = ddata.AVGHUM + "<span>&#8362;</span>"

        if (ddata.AVGBPM === undefined || ddata.AVGBPM == "null" || ddata.AVGBPM == null) {
            bpmelem.innerHTML = "-"
            oxelem.innerHTML = "-"
        }
        else {

            oxelem.innerHTML = ddata.AVGOX + "<span>&#37;</span>"
            bpmelem.innerHTML = ddata.AVGBPM + "<span>&#9829;</span>"
            lastDetectedPulse = new Date();
        }



        // var indexoflabel = undefined
        // for (var i = 0; i < myBarChart.data.labels.length; i++) {

        //     if (myBarChart.data.labels[i] == ddata.DEVICEID)
        //         indexoflabel = i
        // };

        // var pieindexoflabel = undefined
        // for (var i = 0; i < myPieChart.data.labels.length; i++) {

        //     if (myPieChart.data.labels[i] == ddata.DEVICEID)
        //         pieindexoflabel = i
        // };

        // if (myPieChart.data.datasets.length == 0) {
        //     console.log("executing !!!")
        //     myPieChart.data.datasets.push({

        //         "label": "My First Dataset",
        //         "data": [0, 0, 0],
        //         "backgroundColor": ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]

        //     });
        // }
        // if (myBarChart.data.datasets.length == 0) {
        //     myBarChart.data.datasets.push({
        //         label: "Average Temp",
        //         backgroundColor: "rgba(220,220,220,0.5)",
        //         borderColor: "rgba(220,220,220,0.8)",

        //         data: [0, 0, 0]
        //     },
        //         {
        //             label: "Average Hum",
        //             backgroundColor: "rgba(151,187,205,0.5)",
        //             borderColor: "rgba(151,187,205,0.8)",

        //             data: [0, 0, 0]
        //         })

        // }
        // if (indexoflabel === undefined) {
        //     myBarChart.data.labels.push(ddata.DEVICEID)

        // } else {
        //     console.log(myBarChart.data.datasets[0])
        //     myBarChart.data.datasets[0].data[indexoflabel] = ddata.AVGTEMP
        //     myBarChart.data.datasets[1].data[indexoflabel] = ddata.AVGHUM

        // }

        // if (pieindexoflabel === undefined) {

        //     myPieChart.data.labels.push(ddata.DEVICEID)

        // } else {
        //     console.log(myPieChart.data.datasets[0].data)
        //     myPieChart.data.datasets[0].data[pieindexoflabel] = ddata.MINTEMP
        // }
        // myBarChart.update();
        // myPieChart.update();
    };

    ws.onclose = function () {
        output("onclose");
    };

    ws.onerror = function (e) {
        output("onerror");
        console.log(e)
    };
}

function onSubmit() {
    var input = document.getElementById("input");
    // You can send message to the Web Socket using ws.send.
    ws.send(input.value);
    output("send: " + input.value);
    input.value = "";
    input.focus();
}

function onCloseClick() {
    ws.close();
}

function output(str) {
    var log = document.getElementById("log");
    var escaped = str.replace(/&/, "&amp;").replace(/</, "&lt;").
        replace(/>/, "&gt;").replace(/"/, "&quot;"); // "
    //log.innerHTML = escaped + "<br>" + log.innerHTML;
}

function getPatient(e) {
    if (selectedPatientID !== undefined)
        document.getElementById(selectedPatientID).style = ""
    document.getElementById(e).style = "background:red"
    selectedPatientID = e
}



function clock() {
    var clockElement = document.getElementById('clock');
    var m = new Date();
    var dateString =
        m.getUTCFullYear() + "/" +
        ("0" + (m.getUTCMonth() + 1)).slice(-2) + "/" +
        ("0" + m.getUTCDate()).slice(-2) + " " +
        ("0" + m.getUTCHours()).slice(-2) + ":" +
        ("0" + m.getUTCMinutes()).slice(-2) + ":" +
        ("0" + m.getUTCSeconds()).slice(-2);
    clockElement.innerText = dateString;

    if (lastDetectedPulse !== undefined){
        diffPulseSec = Math.abs((new Date() - lastDetectedPulse.getTime()) / 1000)
        textcolor = "cyan"
        if(diffPulseSec>10)
            textcolor = "darkred"
        diffPulseSec = "<span style='color:"+textcolor+"'>last vital signal received "+parseInt(diffPulseSec)+"s ago</span>"
    }
    else {
      
        diffPulseSec = "<span style='color:darkred'>no vital signal, check connection </span>"
    }
    document.getElementById("lastdetected").innerHTML = diffPulseSec
}

setInterval(clock, 1000);
setTimeout(function () {
    // myBarChart.addData([100, 60], "Google");
}, 1000);
