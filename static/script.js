function onPageLoad() {
    const mainPage = "Главная страница";
    const registrationPage = "Регистрация";
    const authPage = "Авторизация";
    const myWordsPage = "Список слов";
    const newTaskPage = "Новое задание";
    const changeAccountDataPage = "Управление аккаунтом";

    const partsOfURL = document.URL.split("/");
    const route = partsOfURL[partsOfURL.length - 1];

    if (route === "") {
        document.getElementById("navbar-heading").innerText = mainPage;
    } else if (route === "register") {
        document.getElementById("navbar-heading").innerText = registrationPage;
    } else if (route === "login") {
        document.getElementById("navbar-heading").innerText = authPage;
    } else if (route === "my_words") {
        document.getElementById("navbar-heading").innerText = myWordsPage;
    } else if (route === "new_task") {
        document.getElementById("navbar-heading").innerText = newTaskPage;
    } else if (route === "change_account_data") {
        document.getElementById("navbar-heading").innerText = changeAccountDataPage;
    } else {
        alert("Not implemented!");
    }

}

window.onload = onPageLoad;
