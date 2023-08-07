$(document).ready(function() {
    $("#add-form").on("click", function(e) {
        e.preventDefault();
        var extraFormsInput = $("#id_extra_forms");
        var numExtraForms = parseInt(extraFormsInput.val(), 10);
        var formsetContainer = $("#formset-container");
        var totalFormsInput = $("#id_form-TOTAL_FORMS");  // Pobierz pole form-TOTAL_FORMS
        var totalForms = parseInt(totalFormsInput.val(), 10);  // Konwertuj na liczbę

        for (var i = 0; i < numExtraForms; i++) {
            var newFormHtml = formsetContainer.find(".mealitem-form:last").html();
            newFormHtml = newFormHtml.replace(/__prefix__/g, totalForms);
            formsetContainer.append('<div class="mealitem-form">' + newFormHtml + '</div>');
            totalForms++;  // Zwiększ liczbę formularzy
        }

        totalFormsInput.val(totalForms);  // Aktualizuj pole form-TOTAL_FORMS
        extraFormsInput.val(1);  // Resetuj pole na 1
    });
});


const AddMoreBtn = document.getElementById('add-more')
const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')

addMoreBtn.addEventListener('click', add_new_form)
function add_new_form(event) {
    if (event) {
    event.preventDefault()
    }
    const currentIngredientForms = document.getElementsByClassName('ingredient-form')
    const currentFormCount = CurrentIngredientForms.length // + 1
    const formCopyTarget = document.getElementById('ingredient-form-list')
    const emptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class', 'ingredient-form')
    copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    // add new empty form element to html form
    formCopyTarget.append(emptyFormEl)
    }