$(document).keydown(function(e) {
  if (e.which === 187) {
    $('#addNewStudent').html("").attr('contenteditable', 'true'); 
    $('#addNewStudent').empty();
    $('#addNewStudent').first().focus();
  }
});

$("#cover").on("change", function() {
  const menu = $(".file");
  const name = $(".file span");
  const cancel = $(".file svg");
  if ($("#cover").val() != ''){
	  name.html($("#cover")[0].files[0].name);
    menu.show();
    cancel.click(function() {
      $("#cover").val(null);
      $(".file").hide();
    });
  }
  else {
    menu.hide();
  }
});

$('#addNewStudent')

.click(function() {
  $(this).html("").attr('contenteditable', 'true');
})

.keyup(function(e) {
  if (e.keyCode === 13) {
    var val = $(this).text();
    $(this)
      .before(`<li id="student" name="student" onclick="this.remove()"><input name="team[]" style="display: none;" value="${val}">${val}</li>`)
      .html(`<img src="./plus.svg">`)
      .attr('contenteditable', 'false');
    e.preventDefault();
  }
});