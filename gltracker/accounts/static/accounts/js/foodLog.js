var calories = document.querySelector('th[data-calories]').getAttribute('data-calories');
var carbohydrates = parseFloat(document.querySelector('th[data-carbohydrates]').getAttribute('data-carbohydrates'));
var fats = parseFloat(document.querySelector('th[data-fats]').getAttribute('data-fats'));
var proteins = parseFloat(document.querySelector('th[data-proteins]').getAttribute('data-proteins'));

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = '#858796';

// Doughnut Chart - Macronutrients breakdown

var total = carbohydrates + fats + proteins

var carbohydratesPercentage =  Math.round((carbohydrates / total) * 100);
var fatsPercentage =  Math.round((fats / total) * 100);
var proteinsPercentage =  Math.round((proteins / total) * 100);

var ctx = document.getElementById('myPieChart');
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: [
            'Carbs ' +  carbohydratesPercentage + '%',
            'Fats ' + fatsPercentage + '%',
            'Proteins ' + proteinsPercentage + '%'
        ],
        datasets:
        [
            {
                data: [carbohydratesPercentage, fatsPercentage, proteinsPercentage],
                backgroundColor: ['#e5a641', '#55b560', '#419ad6'],
            }
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        animation: {
            animateScale: true,
        },
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
            },
            title: {
                display: true,
                text: 'Macronutrients Breakdown',
                font: {
                    size: 20,
                },
            },
            datalabels: {
                display: true,
                color: '#fff',
                font: {
                    weight: 'bold',
                    size: 16,
                },
                textAlign: 'center',
            },
        },
    },
});


// Calorie Goal Progress Bar
// Get the calorie goal from the form input
var calorieGoal = parseFloat(document.querySelector('#id_goals [name="calories"]').value)
var carbohydratesGoal = parseFloat(document.querySelector('#id_goals [name="carbohydrates"]').value)
var fatsGoal = parseFloat(document.querySelector('#id_goals [name="fats"]').value)
var proteinsGoal = parseFloat(document.querySelector('#id_goals [name="proteins"]').value)

// Progress bar helper function
function updateProgressBar(goal, actual, progressBarId, goalText) {
    var percentage = Math.round((actual / goal) * 100);
    var text = (goal === 0)
        ? "<span class='text-primary'>Please set your " + goalText + "</span>"
        : percentage + '%';
    var width = (goal === 0) ? '0%' : percentage + '%';

    $('#' + progressBarId).animate({ width: width }, 500).html(text);
}


// Update Progress bars
updateProgressBar(calorieGoal, calories, 'calorieProgressBar', 'calorie goal');
updateProgressBar(carbohydratesGoal, carbohydrates, 'carbohydratesProgressBar', 'carbohydrates goal');
updateProgressBar(fatsGoal, fats, 'fatsProgressBar', 'fats goal');
updateProgressBar(proteinsGoal, proteins, 'proteinsProgressBar', 'proteins goal');