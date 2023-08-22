const addMoreBtn = document.getElementById('add-more');
const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')

addMoreBtn.addEventListener('click', add_new_form);

function add_new_form(event) {
    if (event) {
        event.preventDefault()
    }
    const currentIngredientForms = document.getElementsByClassName('ingredient-form')
    const currentFormCount = currentIngredientForms.length
    const formCopyTarget = document.getElementById('ingredient-form-list')
    const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class', 'ingredient-form')
    copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(copyEmptyFormEl)
}


