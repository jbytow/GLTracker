$(document).ready(function() {
    $("#add-form").on("click", function(e) {
        e.preventDefault();
        var formsetContainer = $("#formset-container");
        var totalForms = $("#id_form-TOTAL_FORMS").val();

        var newFormHtml = formsetContainer.find(".mealitem-form:last").html();
        newFormHtml = newFormHtml.replace(/__prefix__/g, totalForms);
        formsetContainer.append('<div class="mealitem-form">' + newFormHtml + '</div>');
        totalForms++;
    });

    $(document).on("click", ".remove-form", function(e) {
        e.preventDefault();
        $(this).closest(".mealitem-form").remove();
    });
});