document.querySelector('form').addEventListener('submit', function(event) {
    const password = document.querySelector('input[name="password"]').value;
    const password2 = document.querySelector('input[name="password2"]').value;
    if (length(password.value) < 8) {
        
    }
    let hasDigits = false;
    let hasUpperCase = false;
    let hasLowerCase = false;
    let hasSpecialCharacters = false;
    let hasSpaces = false;
  
    for (let char of password) {
      if (char.isdigit()) {
        hasDigits = true;
      } else if (char.isupper()) {
        hasUpperCase = true;
      } else if (char.islower()) {
        hasLowerCase = true;
      } else if (char === ' ') {
        hasSpaces = true;
      } else {
        hasSpecialCharacters = true;
      }
    }
  
    if (!hasDigits) {
      sendNotification('error', "Пароль должен содержать хотя бы одну цифру");
      event.preventDefault();
      return;
    }
  
    if (!hasUpperCase) {
      sendNotification('error', "Пароль должен содержать хотя бы одну заглавную букву");
      event.preventDefault();
      return;
    }
  
    if (!hasLowerCase) {
      sendNotification('error', "Пароль должен содержать хотя бы одну строчную букву");
      event.preventDefault();
      return;
    }
  
    if (!hasSpecialCharacters) {
      sendNotification('error', "Пароль должен содержать хотя бы один специальный символ");
      event.preventDefault();
      return;
    }
  
    if (hasSpaces) {
      sendNotification('error', "Пароль не должен содержать пробелов");
      event.preventDefault();
      return;
    }
  
    if (password !== password2) {
      sendNotification('error', "Пароли должны совпадать");
      event.preventDefault();
      return;
    }
  });