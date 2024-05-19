const newBtn = document.querySelector("#new")
const newAttributes = {"data-bs-toggle": "modal", "data-bs-target": "#newModal"}
for (const attr in newAttributes) {
    newBtn.setAttribute(attr, newAttributes[attr]);
}

function oneClick(event) {
    words.forEach((elem) => {
        elem.classList.remove("active-td");
    })
    event.target.classList.add("active-td");
}

const words = document.querySelectorAll(".element-in-td");
words.forEach((elem) => {
    elem.addEventListener("click", oneClick);
})

function delWordRequest(wordName, deleted) {
    const url = document.URL.split("/");
    const promise = fetch("/del-word", {
        method: "POST",
        body: JSON.stringify({
            "category": url[url.length - 1],
            "word": wordName
        }),
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
    const words = document.querySelectorAll(".element-in-td");
    for (const w of words) {
        if (w.classList.contains("active-td")) {
            delWordRequest(w.innerText.split(" - ")[0], w);
        }
    }
});
