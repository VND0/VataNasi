async function isUsernameUnique(username) {
    try {
        const promise = await fetch(`http://127.0.0.1:8001/check_unique_uname/${username}`);
    } catch {
        return false;
    }
    const result = await promise.text();
    const returnValue = !!parseInt(result);
    return returnValue;
}

const appendAlert = (message, type) => {
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)
}

function registerUser(newUsername, newPassword) { //TODO: сделать обращение к серверу.
    alert(`${newUsername} with password ${newPassword} wasn't registered.`)
}

function submitRegistration() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmation = document.getElementById("password_confirm").value.trim();

    if (!username || !/^[A-Za-z0-9]*$/.test(username)) {
        let message = "Имя пользователя пустое или содержит недопустимые символы.";
        let errorType = "danger";
        appendAlert(message, errorType)
        return;
    } else if (!isUsernameUnique(username)) {
        let message = "Имя пользователя занято.";
        let errorType = "danger";
        appendAlert(message, errorType)
        return;
    }
    if (!password || password !== confirmation) {
        let message = "Пароли не совпадают.";
        let errorType = "danger";
        appendAlert(message, errorType)
        return;
    }

    registerUser(username, password)
    //TODO: Сделать редирект на главную
}

document.getElementById("submit_registration").onclick = submitRegistration;