function onPageLoad() {
    const mainPage = "Главная страница";
    const registrationPage = "Регистрация";
    const authPage = "Авторизация";
    const myCategoriesPage = "Список категорий";
    const myWordsPage = "Список слов";
    const newTaskPage = "Новое задание";
    const changeAccountDataPage = "Управление аккаунтом";
    const taskPreferencesPage = "Настройка задания";

    const partsOfURL = document.URL.split("/");
    const route = partsOfURL[partsOfURL.length - 1];

    if (route === "") {
        document.getElementById("navbar-heading").innerText = mainPage;
    } else if (route === "register") {
        document.getElementById("navbar-heading").innerText = registrationPage;
    } else if (route === "login") {
        document.getElementById("navbar-heading").innerText = authPage;
    } else if (route === "my_categories") {
        document.getElementById("navbar-heading").innerText = myCategoriesPage;
    } else if (route === "new_task") {
        document.getElementById("navbar-heading").innerText = newTaskPage;
    } else if (route === "change_account_data") {
        document.getElementById("navbar-heading").innerText = changeAccountDataPage;
    } else if (partsOfURL[partsOfURL.length - 2] === "task-preferences") {
        document.getElementById("navbar-heading").innerText = taskPreferencesPage;
    } else if (partsOfURL[partsOfURL.length - 2] === "my_words") {
        document.getElementById("navbar-heading").innerText = myWordsPage;
    } else {
        alert("Not implemented!");
    }

}

window.onload = onPageLoad;
