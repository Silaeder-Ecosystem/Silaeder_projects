function checkFileExtension(fileInput, allowedExtensions) {
  const fileName = fileInput.value;
  const fileExtension = fileName.split('.').pop().toLowerCase();
  return allowedExtensions.includes(fileExtension);
}

document.querySelector('form').addEventListener('submit', async function(event) {
  const jwtCookie = document.cookie.split('; ').find(row => row.startsWith('jwt='));
  if (!jwtCookie) {
    event.preventDefault();
    sendNotification('error', 'Вы не вошли в систему. Пожалуйста, войдите, чтобы продолжить.');
    return;
  }

  var allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];
  var fileInput = document.getElementById('cover');
  
  if (!checkFileExtension(fileInput, allowedExtensions)) {
    event.preventDefault();
    sendNotification('error', 'Неправильный формат файла обложки. Пожалуйста, загрузите файл с допустимым расширением: ' + allowedExtensions.join(', '));
    return;
  }
  allowedExtensions = ['pdf'];
  fileInput = document.getElementById('presentation');
  
  if (!checkFileExtension(fileInput, allowedExtensions)) {
    event.preventDefault();
    sendNotification('error', 'Неправильный формат файла презентации. Пожалуйста, загрузите файл с допустимым расширением: ' + allowedExtensions.join(', '));
    return;
  }

  const validTopics = ['Математика', 'Информатика', 'Машинное обучение', 'Физика', 'Инфобез', 'Экономика', 'Биология', 'Экология', 'Медицина', 'Астрономия', 'Химия', 'Игры', 'Литература', 'История', 'Лингвистика', 'Филология', 'Обществознание', 'Английский', 'География', 'Макетирование'];
  const topicInput = document.getElementById('topic').value;

  if (!validTopics.includes(topicInput)) {
    event.preventDefault();
    sendNotification('error', 'Неправильная секция. Пожалуйста, выберите допустимую секцию: ' + validTopics.join(', '));
    return;
  }

  const teamMembers = document.querySelectorAll('input[name="team[]"]');
  const teacher = document.getElementById('teacher').value;

  if (teamMembers.length === 0) {
    event.preventDefault();
    sendNotification('error', 'Никого нет в проекте. Пожалуйста, добавьте людей в проект');
    return;
  }

  async function fetchUsers(username) {
    const response = await fetch(`http://ilyastarcek.ru:11702/is_user_exists?username=${username}`);
    const users = await response.json();
    return users;
  };
  

  const validateUsers = () => {
    for (let member of teamMembers) {
      const username = member.value;
      fetchUsers(username).then(data => {
        if (!data.exists) {
          sendNotification('error', `Пользователь ${username} не найден. Пожалуйста, проверьте его имя пользователя.`);
          return false;
        }
      });
    }
    
    fetchUsers(teacher).then(data => {
      if (!data.exists) {
        sendNotification('error', `Аккаунт учителя не найден. Пожалуйста, проверьте его имя пользователя.`);
        return false;
      }
    });

    return true;
  };

  const isValid = validateUsers();
  if (!isValid) {
    event.preventDefault();
    return;
  }
});
