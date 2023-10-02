var calories = document.querySelector('th[data-calories]').getAttribute('data-calories');
var carbohydrates = parseFloat(document.querySelector('th[data-carbohydrates]').getAttribute('data-carbohydrates'));
var fats = parseFloat(document.querySelector('th[data-fats]').getAttribute('data-fats'));
var proteins = parseFloat(document.querySelector('th[data-proteins]').getAttribute('data-proteins'));

console.log("Calories:", calories);
console.log("Carbohydrates:", carbohydrates);
console.log("Fats:", fats);
console.log("Proteins:", proteins);


// Calorie Goal Progress Bar

// Get the calorie goal from the form input
var calorieGoal = parseFloat(document.getElementById('id_calorie_goal').value) || 2000; // Default to 2000 if no value or invalid value
console.log("Calorie Goal", calorieGoal)

var caloriePercentage = (calories / calorieGoal) * 100;
console.log("Calorie Percentage", caloriePercentage)

$('.progress-bar').animate({
    width: caloriePercentage + '%',
}, 500);

var interval = setInterval(function () {
    $('.progress-bar').html(caloriePercentage.toFixed(2) + '%');
}, 500);