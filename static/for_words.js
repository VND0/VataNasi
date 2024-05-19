const newBtn = document.querySelector("#new")
const newAttributes = {"data-bs-toggle": "modal", "data-bs-target": "#newModal"}
for (const attr in newAttributes) {
    newBtn.setAttribute(attr, newAttributes[attr]);
}