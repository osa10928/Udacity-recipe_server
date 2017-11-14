$(document).ready(function(){
  $(".add-ingredient-btn").click(showIngredientForm)
  $(".edit-btn").click(showEditIngredientForm)
  $(".cancel-ingredient-btn").click(hideEditIngredientForm)
  $(".delete-ingredient-btn").click(confirmDelete)
})


function showIngredientForm(){
  $('.add-ingredient-btn').css('max-width', '0').css('padding', '0').css('border', 'none');
  $('.add-ingredient-form').css('max-width', '1000px').css('padding', 'initial').css('border', 'initial');
}

function showEditIngredientForm(e){
  let baseId = e.target.id.split("-")[0]
  $("#" + baseId).css('max-width', '0').css('padding', '0').css('border', 'none');
  $("#" + baseId + "-form").css('max-width', '1000px').css('padding', 'initial').css('border', 'initial');
}

function hideEditIngredientForm(e){
  let baseId = e.target.id.split("-")[0]
  $("#" + baseId + "-form").css('max-width', '0').css('padding', '0').css('border', 'none');
  $("#" + baseId).css('max-width', '1000px').css('padding', 'initial').css('border', 'initial');
}

function confirmDelete(e){
  let baseId = e.target.id.split("-")[0]
  let name = $("#" + baseId).children().first().text()
  r = confirm("Are you sure you want to delete the ingredient " + name)
  if (r) {
    console.log($("#" + baseId + "-realdeletebtn").click())
  }
}
