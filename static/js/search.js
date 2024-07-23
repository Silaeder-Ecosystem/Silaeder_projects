const pressed = (e) => {
  if ((window.event ? event.keyCode : e.which) === 13) document.forms[0].submit(input.content);   
}
