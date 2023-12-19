$(".dropdown-actions .is-destroy").on("click", function() {
  const slider = $(this).closest(".dropdown-slider");
  const confirmHeight = slider.find(".dropdown-confirm").outerHeight();
  slider.addClass("show-confirm").height(confirmHeight);
});

$(".dropdown-confirm-actions").on("click", function() {
  const slider = $(this).closest(".dropdown-slider");
  const actionsHeight = slider.find(".dropdown-actions").outerHeight();
  slider.removeClass("show-confirm").height(actionsHeight);
});