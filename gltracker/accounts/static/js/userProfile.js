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
console.log(jsonWeightData);


var weights = jsonWeightData.map(function(record) {
    return record.weight;
});

var entryDates = jsonWeightData.map(function(record) {
    return record.entry_date;
});

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = '#858796';

// Area Chart - Weight History
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: entryDates,
        datasets: [{
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
        }],
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
                    min: 0,
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