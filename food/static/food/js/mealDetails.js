document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('myBarChart');
    const ctx = canvas.getContext('2d');
    const fats = parseFloat(canvas.dataset.fats);
    const carbs = parseFloat(canvas.dataset.carbs);
    const proteins = parseFloat(canvas.dataset.proteins);

    const myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Fat', 'Carbs', 'Protein'],
            datasets: [{
                label: 'Macronutrients (g)',
                data: [fats, carbs, proteins],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

function confirmDelete() {
    var confirmation = confirm("Are you sure you want to delete this meal?");
    if (confirmation) {
        document.getElementById('delete-form').submit();
    }
    return false;
}