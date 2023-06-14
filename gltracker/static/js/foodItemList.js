function sortTable(columnIndex) {
  const table = document.getElementById('food-table');
  const rows = Array.from(table.getElementsByTagName('tr'));

  const sortedRows = rows.slice(1);

  sortedRows.sort((a, b) => {
    const cellA = a.getElementsByTagName('td')[columnIndex].innerText;
    const cellB = b.getElementsByTagName('td')[columnIndex].innerText;
    return cellA.localeCompare(cellB, undefined, { numeric: true, sensitivity: 'base' });
  });

  sortedRows.unshift(rows[0]);

  while (table.firstChild) {
    table.removeChild(table.firstChild);
  }

  sortedRows.forEach(row => {
    table.appendChild(row);
  });
}