function sortTable(columnIndex) {
  let table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("food-table");
  switching = true;

  while (switching) {
    switching = false;
    rows = table.getElementsByTagName("tr");

    for (i = 1; i < rows.length - 1; i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("td")[columnIndex];
      y = rows[i + 1].getElementsByTagName("td")[columnIndex];

      if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
        shouldSwitch = true;
        break;
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}