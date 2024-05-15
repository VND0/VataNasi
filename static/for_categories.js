// const classesWhenNotClicked = "category table-secondary my-3";
// const classesWhenClicked = "category table-info my-3";

function oneClick(event) {
    categories.forEach((elem) => {
        elem.classList.remove("active-td");
    })
    event.target.classList.add("active-td");
}

function doubleClick(event) {

}

const categories = document.querySelectorAll("#categories td");
categories.forEach((el) => {
el.addEventListener("click", oneClick)
el.addEventListener("dblclick", doubleClick)
})