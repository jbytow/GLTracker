//sorting table
function sortTable(tableId, header) {
  const table = document.getElementById(tableId);
  const rows = Array.from(table.getElementsByTagName('tr'));

  const sortedRows = rows.slice(1);

  const columnIndex = parseInt(header.getAttribute('data-column-index'));

  const ascending = table.getAttribute('data-sort') === 'asc';

  sortedRows.sort((a, b) => {
    const cellA = a.getElementsByTagName('td')[columnIndex].innerText;
    const cellB = b.getElementsByTagName('td')[columnIndex].innerText;

    if (ascending) {
      return cellA.localeCompare(cellB, undefined, { numeric: true, sensitivity: 'base' });
    } else {
      return cellB.localeCompare(cellA, undefined, { numeric: true, sensitivity: 'base' });
    }
  });

  table.setAttribute('data-sort', ascending ? 'desc' : 'asc');

  sortedRows.unshift(rows[0]);

  while (table.firstChild) {
    table.removeChild(table.firstChild);
  }

  sortedRows.forEach(row => {
    table.appendChild(row);
  });
}

function deleteFoodItem(foodItemId) {
    // Zapytanie AJAX do usunięcia elementu
    var url = '/food/food_item/delete/' + foodItemId + '/';
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
            // Przekieruj na inną stronę po usunięciu
            window.location.href = '/food/fooditem_list/';
        } else {
            console.error('Błąd podczas usuwania elementu');
        }
    })
    .catch(function(error) {
        console.error('Błąd podczas wysyłania zapytania AJAX:', error);
    });
}