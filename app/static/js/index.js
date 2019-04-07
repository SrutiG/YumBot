function openRecipeModal(recipe_id) {
    $("#" + recipe_id + "-modal").show();
}

function closeRecipeModal(recipe_id) {
    $("#" + recipe_id + "-modal").hide();
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
    console.log("closed modal");
}

function searchRecipes() {
    var ingredient = $("#search-bar").val();
    $.get('/search/' + ingredient, () => {
        window.location.reload();
    })

}

function removeSearch(ingredient) {
    $.get('/remove_search/' + ingredient, () => {
        window.location.reload();
    })
}