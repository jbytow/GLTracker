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
var calorieGoal = parseFloat(document.querySelector('#id_goals [name="calories"]').value) || 2000;
var carbohydratesGoal = parseFloat(document.querySelector('#id_goals [name="carbohydrates"]').value) || 300;
var fatsGoal = parseFloat(document.querySelector('#id_goals [name="fats"]').value) || 70;
var proteinsGoal = parseFloat(document.querySelector('#id_goals [name="proteins"]').value) || 50;

var caloriePercentage = Math.round((calories / calorieGoal) * 100);
var carbohydratesPercentage = Math.round((carbohydrates / carbohydratesGoal) * 100);
var fatsPercentage = Math.round((fats / fatsGoal) * 100);
var proteinsPercentage = Math.round((proteins / proteinsGoal) * 100);

console.log(carbohydratesPercentage)

$('#calorieProgressBar').animate({ width: caloriePercentage + '%' }, 500).html(caloriePercentage + '%');
$('#carbohydratesProgressBar').animate({ width: carbohydratesPercentage + '%' }, 500).html(carbohydratesPercentage + '%');
$('#fatsProgressBar').animate({ width: fatsPercentage + '%' }, 500).html(fatsPercentage + '%');
$('#proteinsProgressBar').animate({ width: proteinsPercentage + '%' }, 500).html(proteinsPercentage + '%');