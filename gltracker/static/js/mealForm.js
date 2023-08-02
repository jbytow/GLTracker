$(document).ready(function() {
    $("#add-form").on("click", function(e) {
        e.preventDefault();
        var extraFormsInput = $("#id_extra_forms");
        var numExtraForms = parseInt(extraFormsInput.val(), 10);
        var formsetContainer = $("#formset-container");
        var totalForms = $("#id_form-TOTAL_FORMS").val();

        for (var i = 0; i < numExtraForms; i++) {
            var newFormHtml = formsetContainer.find(".mealitem-form:last").html();
            newFormHtml = newFormHtml.replace(/__prefix__/g, totalForms);
            formsetContainer.append('<div class="mealitem-form">' + newFormHtml + '</div>');
            totalForms++;
        }

        extraFormsInput.val(1);  // Resetuj pole na 1
    });
});