function onPageLoad() {
    const mainPage = "Главная страница";
    const registrationPage = "Регистрация";
    const authPage = "Авторизация";
    const myWordsPage = "Список слов";
    const newTaskPage = "Новое задание";

    const partsOfURL = document.URL.split("/");
    const route = partsOfURL[partsOfURL.length - 1];

    switch (route) {
        case "":
            document.getElementById("navbar-heading").innerText = mainPage;
            break;
        case "register":
            document.getElementById("navbar-heading").innerText = registrationPage;
            break;
        case "login":
            document.getElementById("navbar-heading").innerText = authPage;
            break;
        case "my_words":
            document.getElementById("navbar-heading").innerText = myWordsPage;
            break;
        case "new_task":
            document.getElementById("navbar-heading").innerText = newTaskPage;
            break;
    }
}

window.onload = onPageLoad;
