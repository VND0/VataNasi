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

function delCategoryRequest(catName, deleted) {
    const promise = fetch("/del-category", {
        method: "POST",
        body: JSON.stringify({"category_name": catName}),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
    }).then((response) => {
        console.log(response.text());
    }).then((response) => {
        deleted.parentNode.remove();
        location.reload();

    })
}

document.querySelector("#delete").addEventListener("click", (event) => {
    const categories = document.querySelectorAll(".category-in-td");
    for (const c of categories) {
        if (c.classList.contains("active-td")) {
            delCategoryRequest(c.innerText, c);
        }
    }
});

const newBtn = document.querySelector("#new")
const newAttributes = {"data-bs-toggle": "modal", "data-bs-target": "#newModal"}
for (const attr in newAttributes) {
    newBtn.setAttribute(attr, newAttributes[attr]);
}