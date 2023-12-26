$(document).mouseup(function (e) {
  const container = $(".column");
  if (container.has(e.target).length === 0){
    container.hide();
  }
});
$(document).mouseup(function (e) {
  const container = $(".delete-column");
  if (container.has(e.target).length === 0){
    container.hide();
  }
});
$(".more").on("click", function() {
  const menu = $(".column");
  const more = $(".more");
  const num = $(this).attr("class").split(" ")[1].toString();
  const tableView = $(`.table-link-view.${num}`).attr("href").toString();
  const tableEdit = $(`.table-link-edit.${num}`).attr("href").toString();
  const tableDelete = $(`.trash.${num}`).attr("link").toString();
  $(`.dropdown-link-view`).attr("href", tableView); 
  $(`.dropdown-link-edit`).attr("href", tableEdit); 
  $(`.dropdown-link-delete`).attr("href", tableDelete); 
  menu.show();
})
$(".trash").on("click", function() {
  const menu = $(".delete-column");
  const trash = $(".trash");
  const num = $(this).attr("class").split(" ")[1].toString();
  const tableDelete = $(`.trash.${num}`).attr("link").toString();
  $(`.table-link-delete`).attr("href", tableDelete); 
  menu.show();
})
$(".action.cancel").on("click", function() {
  const menu = $(".delete-column");
  menu.hide()
})