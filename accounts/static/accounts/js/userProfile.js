function deleteWeightRecord(weightRecordId) {
    var confirmation = confirm("Are you sure you want to delete that weight record?");
    if (confirmation) {
        var url = '/accounts/profile/delete/' + weightRecordId + '/';
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then(function(response) {
            if (response.ok) {
                window.location.href = '/accounts/profile/';
            } else {
                console.error('Error during removal of the element');
            }
        })
        .catch(function(error) {
            console.error('Error during sending AJAX query:', error);
        });
    }
}

var jsonWeightData = JSON.parse(document.getElementById("weight-data").textContent);
jsonWeightData.reverse()
console.log(jsonWeightData);


var weights = jsonWeightData.map(function(record) {
    return record.weight;
});

var entryDates = jsonWeightData.map(function(record) {
    return record.entry_date;
});

var target_weight = document.getElementById('myChart').getAttribute('data-target-weight');
console.log(target_weight)

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = '#858796';

// Area Chart - Weight History
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    type: 'line',
    data: {
        labels: entryDates,
        datasets: [
            {
                label: 'Weight',
                data: weights,
                lineTension: 0.3,
                backgroundColor: 'rgba(2,117,216,0.2)',
                borderColor: 'rgba(2,117,216,1)',
                pointRadius: 5,
                pointBackgroundColor: 'rgba(2,117,216,1)',
                pointBorderColor: 'rgba(255,255,255,0.8)',
                pointHoverRadius: 5,
                pointHoverBackgroundColor: 'rgba(2,117,216,1)',
                pointHitRadius: 50,
                pointBorderWidth: 2,
            },
            {
                label: 'Target Weight',
                data: Array(entryDates.length).fill(target_weight),
                borderColor: 'rgba(0, 128, 0, 1)',
                pointBorderColor: 'rgba(0, 128, 0, 1)',
                pointBackgroundColor: 'rgba(0, 128, 0, 1)',
                borderDash: [5, 5],
                borderWidth: 2,
                fill: false,
            },
        ],
    },
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    autoSkip: false,
                    maxRotation: 60,
                    minRotation: 60
                },
                gridLines: {
                    display: true
                },
                scaleLabel: {
                    display: true,
                    padding: 10,
                    fontColor: '#555759',
                    fontSize: 16,
                    fontStyle: 700,
                    labelString: 'Date'
                },
            }],
            yAxes: [{
                ticks: {
                    min: 40,
                    max: 120,
                    maxTicksLimit: 12,
                    padding: 10,
                    // Include a 'kg' in the ticks
                    callback: function(value, index, values) {
                        return value + 'kg';
                    }
                },
                gridLines: {
                    color: "rgba(0, 0, 0, .125)",
                },
                scaleLabel: {
                    display: true,
                    padding: 10,
                    fontColor: '#555759',
                    fontSize: 16,
                    fontStyle: 700,
                    labelString: 'Weight in kg'
                },
            }],
        },
        legend: {
            display: false
        }
    }
});

document.getElementById('date-range').addEventListener('change', function() {
    var selectedRange = this.value; // Download the data range

    var today = new Date(); // get today's data
    var filteredWeights = [];
    var filteredEntryDates = [];

    // Start data for period
    var startDate = new Date();
    switch (selectedRange) {
        case '1-month':
            startDate.setMonth(today.getMonth() - 1);
            break;
        case '3-months':
            startDate.setMonth(today.getMonth() - 3);
            break;
        case '6-months':
            startDate.setMonth(today.getMonth() - 6);
            break;
        case '1-year':
            startDate.setFullYear(today.getFullYear() - 1);
            break;
        case '2-years':
            startDate.setFullYear(today.getFullYear() - 2);
            break;
        case '3-years':
            startDate.setFullYear(today.getFullYear() - 3);
            break;
        case 'all':
            startDate = new Date(1900, 0, 1);
            break;
    }

    // filter the data on the range
    for (var i = 0; i < jsonWeightData.length; i++) {
        var entryDate = new Date(jsonWeightData[i].entry_date);

        if (entryDate >= startDate && entryDate <= today) {
            filteredWeights.push(jsonWeightData[i].weight);
            filteredEntryDates.push(jsonWeightData[i].entry_date);
        }
    }

    myChart.data.labels = filteredEntryDates;
    myChart.data.datasets[0].data = filteredWeights;
    myChart.update();
});