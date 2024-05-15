function oneClick(event) {
    categories.forEach((elem) => {
        elem.classList.remove("active-td");
        console.log(elem)
    })
    event.target.classList.add("active-td");
    console.log(event.target)
}

function doubleClick(event) {

}

const categories = document.querySelectorAll(".category-in-td");

categories.forEach((elem) => {
    elem.addEventListener("click", oneClick)
    elem.addEventListener("dblclick", doubleClick)
})

function delCategoryRequest() {

}

document.querySelector("#delete").addEventListener("click", (event) => {
    const categories = document.querySelectorAll(".category-in-td");
    for (const c of categories) {
        if ("active-td" in c.classList) {
            //TODO: доделать функцию
        }
    }
})