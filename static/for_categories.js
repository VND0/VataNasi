function oneClick(event) {
    categories.forEach((elem) => {
        elem.classList.remove("active-td");
    })
    event.target.classList.add("active-td");
}

function doubleClick(event) {

}

const categories = document.querySelectorAll(".category-in-td");

categories.forEach((elem) => {
    elem.addEventListener("click", oneClick)
    elem.addEventListener("dblclick", doubleClick)
})

function delCategoryRequest(catName) {
    const promise = fetch("/del-category", {
        method: "POST",
        body: JSON.stringify({"category_name": catName}),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
    }).then((response) => {
        console.log(response.text());
    })
}

document.querySelector("#delete").addEventListener("click", (event) => {
    const categories = document.querySelectorAll(".category-in-td");
    for (const c of categories) {
        if (c.classList.contains("active-td")) {
            delCategoryRequest(c.innerText);
            location.reload(); //TODO: пофиксить то, что надо отдельно перезагружать страницу
        }
    }
})