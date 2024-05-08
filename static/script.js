const mainPageLink = "/";
const registerPageLink = "/register"
const loginPageLink = "/login"

function isLoggedIn() {
    return false; // TODO: Реализовать, когда будет вход
}

function dropdownWhenLoggedIn() {
    const parent = document.getElementById("account-dropdown-menu");
    const new_content = `<ul class="dropdown-menu">
<li><a class="dropdown-item" href="#">Изменить данные</a></li>
<li>
<hr class="dropdown-divider">
</li>
<li><a class="dropdown-item" href="#">Выйти</a></li>
<li><a class="dropdown-item" href="#">Удалить аккаунт</a></li>
</ul>`;
    parent.insertAdjacentHTML("beforeend", new_content);

    console.log("Содержимое меню аккаунта вставлено");
}

function dropdownWhenNotLoggedIn() {
    const parent = document.getElementById("account-dropdown-menu");
    const new_content = `<ul class="dropdown-menu">
<li><a class="dropdown-item" href="${loginPageLink}">Войти</a></li>
<li><a class="dropdown-item" href="${registerPageLink}">Зарегистрироваться</a></li>
</ul>`;
    parent.insertAdjacentHTML("beforeend", new_content);

    console.log("Содержимое меню аккаунта вставлено");
}

function linksToWordsAndTaskWhenLoggedIn() {
    //TODO: настроить ссылки на навбаре
}

function linksToWordsAndTaskWhenNotLoggedIn() {
    const toMyWords = document.getElementById("my-words-link");
    const toNewTask = document.getElementById("new-task-link");

    toMyWords.href = "http://127.0.0.1:8000/login";
    toNewTask.href = "http://127.0.0.1:8000/login";
}

document.getElementById("main-page-logo").href = mainPageLink;
if (isLoggedIn()) {
    dropdownWhenLoggedIn();
    linksToWordsAndTaskWhenLoggedIn();
} else {
    dropdownWhenNotLoggedIn();
    linksToWordsAndTaskWhenNotLoggedIn(); //TODO: перенести на flask
}