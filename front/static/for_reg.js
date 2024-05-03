function isUsernameUnique(username) {
    // let responseText = undefined;
    // try {
    //     const promise = fetch(`http://127.0.0.1:8001/check_unique_uname/${username}`).
    //     then((prom) => {responseText = prom.text()});
    // } catch {
    //     return false;
    // }
    // while (responseText === undefined) {
    // }
    //
    // return !!parseInt(responseText);
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `http://127.0.0.1:8001/check_unique_uname/${username}`, false);
    xhr.send();
    return !!parseInt(xhr.responseText); //TODO: обрабатывать статус код
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

function registerUser(newUsername, newPassword) {
    // alert(`${newUsername} with password ${newPassword} wasn't registered.`)
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8001/reg", false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const userData = {
        username: newUsername,
        password: newPassword,
    }
    xhr.send(JSON.stringify(userData));

    alert(xhr.responseText); //TODO: сделать нормально
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
    location.replace("/");
}

document.getElementById("submit_registration").onclick = submitRegistration;