///////////////////////// Automated Watering /////////////////////////
const autoSwitch = document.getElementById("autoSwitch");
const manualSwitch = document.getElementById("manualSwitch");
const runTestSwitch = document.getElementById("runTest");

const addTestDeviceBtn = $('#addTestDeviceBtn');
addTestDeviceBtn.click(function () {
    addTestDevice();
    window.location = window.location.href;
})

function addTestDevice() {
    $.ajax({
        url: "/api/addTestDevice",
    })
}

const deleteTestDeviceBtn = $('#deleteTestDeviceBtn');
deleteTestDeviceBtn.click(function () {
    deleteTestDevice();
})

function deleteTestDevice() {
    $.ajax({
        url: "/api/deleteTestDevice",
    })
}

function getStatus() {
    jQuery.ajax({
        url: "/api/status",
        type: "POST",
        success: function (ndata) {
            // console.log(ndata[0].status);
            let status = ndata[0].status;
            if (status == "A") {
                autoSwitch.checked = true;
                manualSwitch.disabled = true;
                manualSwitch.checked = false;
            } else if (status == "M" || status == "F") {
                autoSwitch.checked = false;
                manualSwitch.checked = false;
            } else if (status == "O") {
                autoSwitch.checked = false;
                manualSwitch.checked = true;
            } else {
                autoSwitch.checked = true;
                manualSwitch.disabled = true;
                manualSwitch.checked = false;
            }
        }
    })
}

function getTestStatus() {
    jQuery.ajax({
        url: "/api/testStatus",
        type: "POST",
        success: function (ndata) {
            console.log(ndata[0].testStatus);
            let testStatus = ndata[0].testStatus;
            if (testStatus == "Y") {
                runTestSwitch.checked = true;
            } else {
                runTestSwitch.checked = false;
            }
        }
    })
}

function auto() {
    let autoStatus;
    if (autoSwitch.checked) {
        autoStatus = "A";
        manualSwitch.disabled = true;
        manualSwitch.checked = false;
    } else {
        autoStatus = "M";
        manualSwitch.disabled = false;
    }
    // console.log(autoStatus);

    $.ajax({
        url: "changeStatus/" + autoStatus
    })

}

function manual() {
    let manualStatus;
    if (manualSwitch.checked) {
        manualStatus = "O";
    } else {
        manualStatus = "F";
    }
    // console.log(manualStatus);
    $.ajax({
        url: "changeStatus/" + manualStatus
    })
}

function runTest() {
    let run;
    if (runTestSwitch.checked) {
        run = "Y";
    } else {
        run = "N";
    }
    // console.log("run = ",run);
    $.ajax({
        url: "runTest/" + run
    })
}


///////////////////////// Get readings /////////////////////////
function getData() {
    jQuery.ajax({
        url: "/api/getData",
        type: "POST",
        success: function (ndata) {
            console.log(ndata);
            tempValue = ndata[0].temperature;
            humValue = ndata[0].humidity;
            soilValue = ndata[0].moisture;
            lightValue = ndata[0].light;

            $('#tempValue').html(tempValue);
            $('#humValue').html(humValue);
            $('#soilValue').html(soilValue);
            $('#lightValue').html(lightValue);
        }
    })
}

///////////////////////// Get testData /////////////////////////
function getTestData() {
    jQuery.ajax({
        url: "/api/getTestData",
        type: "POST",
        success: function (ndata) {
            console.log(ndata);
            let deviceCount = Object.keys(ndata[0]).length;
            // console.log('deviceCount = ',deviceCount);
            let i;
            for (i = 2; i < deviceCount; i++) {
                let test = Object.values(ndata[0])[i];
                console.log('test = ', test)
                $(`#test${i-1}`).html(test);
            }
        }
    })
}

/////////////////////// Get Chart data ///////////////////////
function getChartData() {
    jQuery.ajax({
        url: "/api/getChartData",
        type: "POST",
        success: function (ndata) {
            // console.log(ndata)
            const chartData = ndata;
            // console.log("Getting Chart data")

            let tempArr = [];
            let humArr = [];
            let soilArr = [];
            let lightArr = [];
            let timeArr = [];

            chartData.forEach((e) => {
                tempArr.push(e.temperature);
                humArr.push(e.humidity);
                soilArr.push(e.moisture);
                lightArr.push(e.light);

                let datetime = e.datetimeid;
                // console.log(datetime);
                jsdatetime = new Date(Date.parse(datetime));
                jstime = jsdatetime.toLocaleTimeString();
                timeArr.push(jstime);
            })

            createGraph(tempArr, timeArr, '#tempChart');
            createGraph(humArr, timeArr, '#humChart');
            createGraph(soilArr, timeArr, '#soilChart');
            createGraph(lightArr, timeArr, '#lightChart');

        }
    })
}

// Charts
function createGraph(data, newTime, newChart) {

    let chartData = {
        labels: newTime,
        series: [data]
    };
    // console.log(chartData);

    let options = {
        axisY: {
            onlyInteger: true
        },
        fullWidth: true,
        width: '100%',
        height: '100%',
        lineSmooth: true,
        chartPadding: {
            right: 50
        }
    };

    new Chartist.Line(newChart, chartData, options);

}

/////////////////////// run functions ///////////////////////
$(document).ready(function () {
    getData();
    getTestData();
    getStatus();
    getTestStatus();
    getChartData();

    setInterval(function () {
        getData();
        getTestData();
        getChartData();
    }, 5000);
})