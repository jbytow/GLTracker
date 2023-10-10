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

  // add class 'manual-striped' for very 1st, 'manual-hover' for every row
  for(let i = 0; i < sortedRows.length; i++) {
    if (i % 2 === 1) {
      sortedRows[i].classList.remove('manual-striped');
    } else {
      sortedRows[i].classList.add('manual-striped');
    }

    sortedRows[i].classList.add('manual-hover');
  }

  sortedRows.unshift(rows[0]);

  while (table.firstChild) {
    table.removeChild(table.firstChild);
  }

  sortedRows.forEach(row => {
    table.appendChild(row);
  });

}

//deleting FoodItems
function deleteFoodItem(foodItemId) {
    var confirmation = confirm("Are you sure you want to delete that product?");
    if (confirmation) {
        var url = '/food/fooditem/delete/' + foodItemId + '/';
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            } else {
                console.error('Error during removal of the element');
            }
        })
        .catch(function(error) {
            console.error('Error during sending AJAX query:', error);
        });
    }
}