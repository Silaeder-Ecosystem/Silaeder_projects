$(document).keydown(function(e) {
  if (e.which === 187) {
    $('#addNewStudent').html("").attr('contenteditable', 'true'); 
    $('#addNewStudent').empty();
    $('#addNewStudent').first().focus();
  }
});

$(document).ready(function() {
  $("#cover").on("change", function() {
    const fileInput = $(this);
    const fileName = fileInput[0].files[0].name;
    const fileDisplay = fileInput.next(".file");
    const fileNameSpan = fileDisplay.find("span");
    const cancelIcon = fileDisplay.find("i");

    if (fileName) {
      fileNameSpan.text(fileName);
      fileDisplay.show();
    } else {
      fileDisplay.hide();
    }

    cancelIcon.on("click", function() {
      fileInput.val(null);
      fileNameSpan.text("");
      fileDisplay.hide();
    });
  });

  $("#presentation").on("change", function() {
    const fileInput = $(this);
    const fileName = fileInput[0].files[0].name;
    const fileDisplay = fileInput.next(".file");
    const fileNameSpan = fileDisplay.find("span");
    const cancelIcon = fileDisplay.find("i");

    if (fileName) {
      fileNameSpan.text(fileName);
      fileDisplay.show();
    } else {
      fileDisplay.hide();
    }

    cancelIcon.on("click", function() {
      fileInput.val(null);
      fileNameSpan.text("");
      fileDisplay.hide();
    });
  });
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
      .html(`<img src="/static/image/plus.svg">`)
      .attr('contenteditable', 'false');
    e.preventDefault();
  }
});