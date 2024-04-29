function isLoggedIn() {
    return false; // TODO: Реализовать, когда будет вход
}

function dropdownWhenLoggedIn() { //TODO: Реализовать норм ссылки на кнопках.
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

function dropdownWhenNotLoggedIn() { //TODO: Реализовать норм ссылки на кнопках.
    const parent = document.getElementById("account-dropdown-menu");
    const new_content = `<ul class="dropdown-menu">
<li><a class="dropdown-item" href="#">Войти</a></li>
<li><a class="dropdown-item" href="#">Зарегистрироваться</a></li>
</ul>`;
    parent.insertAdjacentHTML("beforeend", new_content);

    console.log("Содержимое меню аккаунта вставлено");
}

if (isLoggedIn()) {
    dropdownWhenLoggedIn();
} else {
    dropdownWhenNotLoggedIn();
}